import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.core import Applications
from src.infrastructure.tools import run_tool
from src.core.base import BaseCore
from src.infrastructure.tools.tools_generator import FunctionToOpenAITool
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.infrastructure.completion_parser import ParserType, JsonParser
from src.schemas import ChatMessageSchema, PromptSchema, AskAboutSchema
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.repositories import AskAboutRepository, OrgRepository, DealRepository
from src.prompts.ask_about_deal import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT, QUESTION
from src.schemas.models import (
    ChatAnthropicClaude3Haiku,
    ChatOpenaiGpt4o,
    ChatCohereCommandLightNightly,
    ChatOpenaiGpt35,
    ChatOpenaiGpt4Turbo,
)

logger = logging.getLogger(__name__)


class AskAboutDeal(BaseCore):
    def __init__(self, db_session: Session, inputs: AskAboutSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.ask_about_deal.value)
        self.inputs = inputs
        self.fetch_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt4Turbo())

    @classmethod
    def output_type_router(cls, query: str, query_type: str) -> tuple[str, str]:
        """
        determine which type of query it is along the query to perform. Should it return a 'slide', 'image', 'text'.

        :param query: The `query` parameter is a string that represents the query being passed to the
        router function. In this case, the function is designed to handle queries related to images
        :type query: str
        :param query_type: query_type is a parameter that specifies the type of query being passed to
        the router function. In this case, it is a string indicating whether the query is 'slide', 'image', 'text'
        :type query_type: str
        """
        return query, query_type

    def trim_context(self, text: str) -> str:
        max_user_message_len = (
            ChatOpenaiGpt4Turbo().context_size - self.system_prompt_len - ChatOpenaiGpt4Turbo().max_output
        )

        return self.tokenizer.get_last_n_tokens(text, n=max_user_message_len)

    def build_chat(self) -> ChatSchema:
        return ChatSchema(
            deal_id=self.inputs.deal_id,
            org_id=self.inputs.org_id,
            user_id=self.inputs.user_id,
            chat_type=self.chat_type,
        )

    def enrich_base_model(self, parsed_completion: ParserType) -> AskAboutSchema:
        input = self.inputs
        input.answer = parsed_completion.parsed_completion.get("answer")
        input.chat_id = self.build_chat().id
        input.org_name = OrgRepository(self.db_session).read(input.org_id).name
        input.deal_name = DealRepository(self.db_session).read(input.deal_id).name
        input.modality = None
        input.intent = None

        return input

    def is_correct_prediction(self, parsed_completion: ParserType) -> bool:
        confidence = parsed_completion.parsed_completion.get("confidence", 0)
        answer = parsed_completion.parsed_completion.get("answer", "idk")
        if not isinstance(confidence, int):
            confidence = int(confidence) if confidence.isdigit() else 0
        if confidence >= 1 and answer != "idk":
            return True

        return False

    def chat_completion(self, messages: list[ChatMessageSchema]) -> PromptSchema:
        try:
            try:
                return OpenaiChat(ChatOpenaiGpt4Turbo()).predict(messages, response_format="json_object")
            except Exception as e:
                logger.error(f"Openai chat_completion error {e}", extra={"error": e})
                return AnthropicChat(ChatAnthropicClaude3Haiku()).predict(messages)
        except Exception as e:
            logger.error(f"Anthropic chat_completion error {e}", extra={"error": e})
            return CohereChat(ChatCohereCommandLightNightly()).predict(messages)

    def parse_completion(self, completion: str) -> ParserType:
        return JsonParser.parse(text=completion)

    def determing_output_type(self, query: str) -> tuple[str, str]:
        tool_transformer = FunctionToOpenAITool(self.output_type_router).generate_tool_json()
        messages = [
            ChatMessageSchema(
                role="system",
                message="You are an ai assistant that reroute the query to the correct output format, please use the provided tool",
            ),
            ChatMessageSchema(role="user", message=query),
        ]
        prediction = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
        func_result = run_tool(prediction.tools_call, {"output_type_router": self.output_type_router})
        if not func_result:
            return query, "text"
        else:
            return func_result[0], func_result[1]

    def update_query(self, query: str) -> tuple[str, str]:
        messages = [
            ChatMessageSchema(
                role="system",
                message="""
**System Prompt: Chain of Thought for Query Transformation**

**Objective:** Transform complex or broad queries into simpler, more focused queries to improve retrieval accuracy and efficiency.

**Instructions:**

1.  **Receive the Input Query:** Take the initial complex or broad query as input.

2.  **Understand the Query:** Break down the query into its core components to understand its intent and scope.

3.  **Identify Key Concepts:** Identify key concepts, terms, or entities within the query that are essential for accurate information retrieval.

4.  **Generate Sub-Queries:** Based on the identified key concepts, generate one or more simpler sub-queries that individually address different aspects of the original query.

5.  **Maintain Relevance:** Ensure that each sub-query is relevant and directly related to the original query's intent. The sub-queries should collectively cover all aspects of the initial query.

6.  **Return the Sub-Queries:** Output the transformed sub-queries.


**Example:**

*   **Input Query:** "What are the latest advancements in AI for medical diagnostics and how are they being implemented in hospitals?"

*   **Chain of Thought Process:**

    1.  Understand the query: Focus on advancements in AI for medical diagnostics and their implementation in hospitals.
    2.  Identify key concepts: "latest advancements in AI," "medical diagnostics," "implementation in hospitals."
    3.  Generate sub-queries:
        *   "What are the latest advancements in AI for medical diagnostics?"
        *   "How are AI advancements being implemented in hospitals for medical diagnostics?"
*   **Output Sub-Queries:**

    *   "What are the latest advancements in AI for medical diagnostics?"
    *   "How are AI advancements being implemented in hospitals for medical diagnostics?"

**End of System Prompt**
                """,
            ),
            ChatMessageSchema(role="user", message=query),
        ]
        prediction = OpenaiChat(ChatOpenaiGpt4o()).predict(messages)
        logger.info(prediction.prediction)

    def predict(self, text: str, query: str, **kwargs) -> AskAboutSchema:
        message_system = self.fill_string(
            SYSTEM_MSG,
            [
                ("$ORG_NAME", self.org),
                ("$DEAL_NAME", self.deal),
                ("$EXAMPLES", EXAMPLE),
            ],
        )
        self.system_prompt_len = self.tokenizer.length_function(message_system)
        self.update_query(query=query)
        # query, output_type = self.determing_output_type(query=query)
        # self.inputs.output_type = output_type
        # message_user = self.fill_string(USER_MSG, [("$INPUT", self.trim_context(text)), ("$QUESTION", query)])
        # prediction = self.run_thread(message_system=message_system, message_user=message_user, last_n_messages=0)

        # return prediction

    def store_to_db_base_model(self, input: AskAboutSchema) -> AskAboutSchema:
        return AskAboutRepository(self.db_session).create(input)


if __name__ == "__main__":
    from src.schemas import DealSchema, OrgSchema
    from src.repositories import OrgRepository, DealRepository
    from src.db.db import get_session

    inputs = AskAboutSchema(
        user_id="a689a31e-e63c-532c-9631-ebd39b9c5534",
        creator_type="simlation",
        qa_type="deal",
        deal_id="91038e80-3b23-5ada-b684-04309119da20",
        org_id="383a829a-9fe4-5368-8d6f-254530c37242",
    )
    db_session = get_session()
    db_org = OrgRepository(db_session).read(inputs.org_id)
    if not db_org:
        db_org = OrgRepository(db_session).create(OrgSchema(name="org_name", status="active", creator_type="user"))
    db_deal = DealRepository(db_session).read(inputs.deal_id)
    if not db_deal:
        db_deal = DealRepository(db_session).create(
            DealSchema(name="deal_name", org_id=db_org.id, status="active", creator_type="user")
        )
    AskAboutDeal(db_session, inputs).predict(INPUT, QUESTION)
