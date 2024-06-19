import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.infrastructure.completion_parser import ParserType, JsonParser
from src.schemas import ChatMessageSchema, PromptSchema, AskAboutSchema
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.repositories import AskAboutRepository, OrgRepository, DealRepository
from src.prompts.ask_about_deal import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT, QUESTION
from src.schemas.models import (
    ChatAnthropicClaude3Haiku,
    ChatCohereCommandLightNightly,
    ChatOpenaiGpt4Turbo,
)

logger = logging.getLogger(__name__)


class AskAboutDeal(BaseCore):
    def __init__(self, db_session: Session, inputs: AskAboutSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.ask_about_deal.value)
        self.inputs = inputs
        self.fetch_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt4Turbo())
        self.last_n_messages = 2

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
        message_user = self.fill_string(USER_MSG, [("$INPUT", self.trim_context(text)), ("$QUESTION", query)])
        prediction = self.run_thread(message_system=message_system, message_user=message_user, last_n_messages=0)

        return prediction

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
        question=QUESTION,
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
