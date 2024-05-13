import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.repositories import DealKnowledgeExtractionRepository
from src.infrastructure.completion_parser import ParserType, ListParser
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.prompts.deal_knowledge_extraction import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT
from src.schemas import ChatMessageSchema, PromptSchema, DealKnowledgeExtractionSchema
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly

logger = logging.getLogger(__name__)


class DealKnowledgeExtraction(BaseCore):
    def __init__(self, db_session: Session, inputs: DealKnowledgeExtractionSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.deal_knowledge_extraction.value)
        self.inputs = inputs
        self.fetch_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt35())

    def trim_context(self, text: str) -> str:
        max_user_message_len = (
            ChatOpenaiGpt35().context_size - self.system_prompt_len - ChatOpenaiGpt35().max_output - 1024
        ) // 2

        return self.tokenizer.get_last_n_tokens(text, n=max_user_message_len)

    def build_chat(self) -> ChatSchema:
        return ChatSchema(deal_id=self.inputs.deal_id, org_id=self.inputs.org_id, chat_type=self.chat_type)

    def enrich_base_model(self, parsed_completion: ParserType) -> list[DealKnowledgeExtractionSchema]:
        return [self.prediction_to_knowledge_graph(knowledge) for knowledge in parsed_completion.parsed_completion]

    def is_correct_prediction(self, parsed_completion: ParserType) -> bool:
        return bool(isinstance(parsed_completion.parsed_completion, list))

    def chat_completion(self, messages: list[ChatMessageSchema]) -> PromptSchema:
        try:
            try:
                return OpenaiChat(ChatOpenaiGpt35()).predict(messages)
            except Exception as e:
                logger.error(f"Openai chat_completion error {e}", extra={"error": e})
                return AnthropicChat(ChatAnthropicClaude3Haiku()).predict(messages)
        except Exception as e:
            logger.error(f"Anthropic chat_completion error {e}", extra={"error": e})
            return CohereChat(ChatCohereCommandLightNightly()).predict(messages)

    def parse_completion(self, completion: str) -> ParserType:
        return ListParser.parse(text=completion)

    def prediction_to_knowledge_graph(self, knowledge: dict):
        def build_text_from_knowledge(knowledge: dict) -> str:
            return f"{knowledge.get('subject')} {knowledge.get('predicate')} {knowledge.get('object')}"

        input = self.inputs.model_copy()
        input.meeting_timestamp = knowledge.pop("timestamp") if "timestamp" in knowledge else None
        input.knowledge_text = build_text_from_knowledge(knowledge)
        input.knowledge = knowledge
        input.set_id()

        return input

    def predict(self, text: str, **kwargs) -> list[DealKnowledgeExtractionSchema]:
        message_system = self.fill_string(
            SYSTEM_MSG, [("$ORG_NAME", self.org), ("$DEAL_NAME", self.deal), ("$EXAMPLES", EXAMPLE)]
        )
        self.system_prompt_len = self.tokenizer.length_function(message_system)
        message_user = self.fill_string(USER_MSG, [("$INPUT", self.trim_context(text))])
        prediction = self.run_thread(message_user=message_user, message_system=message_system, last_n_messages=0)

        return prediction

    def store_to_db_base_model(self, input: list[DealKnowledgeExtractionSchema]) -> list[DealKnowledgeExtractionSchema]:
        return [DealKnowledgeExtractionRepository(self.db_session).create(x) for x in input]


if __name__ == "__main__":
    from src.repositories import BotRepository, DealRepository, OrgRepository
    from src.schemas import DealSchema, BotSchema, OrgSchema
    from src.db.db import get_session

    inputs = DealKnowledgeExtractionSchema(
        bot_id="153585b1-883a-5cc9-a443-510b99764841",
        deal_id="91038e80-3b23-5ada-b684-04309119da20",
        org_id="383a829a-9fe4-5368-8d6f-254530c37242",
        seconds_ago=None,
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
    db_bot = BotRepository(db_session).read(inputs.bot_id)
    if not db_bot:
        db_bot = BotRepository(db_session).create(BotSchema(id=inputs.bot_id, deal_id=db_deal.id, org_id=db_org.id))
    DealKnowledgeExtraction(db_session, inputs).predict(INPUT)
