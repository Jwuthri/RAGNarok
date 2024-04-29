import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.infrastructure.completion_parser import JsonParser
from src.repositories import LiveQuestionExtractionRepository
from src.infrastructure.completion_parser.base import ParserType
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.prompts.live_question_extraction import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT
from src.schemas.models import ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly
from src.schemas import ChatMessageSchema, ChatOpenaiGpt35, PromptSchema, LiveQuestionExtractionSchema

logger = logging.getLogger(__name__)


class LiveQuestionExtraction(BaseCore):
    def __init__(self, db_session: Session, inputs: LiveQuestionExtractionSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.live_question_extraction.value)
        self.inputs = inputs
        self.set_company_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt35())

    def trim_context(self, text: str) -> str:
        max_user_message_len = (
            ChatOpenaiGpt35().context_size - self.system_prompt_len - ChatOpenaiGpt35().max_output - 1024
        ) // 2

        return self.tokenizer.get_last_n_tokens(text, n=max_user_message_len)

    def build_chat(self) -> ChatSchema:
        return ChatSchema(
            bot_id=self.inputs.bot_id, deal_id=self.inputs.deal_id, org_id=self.inputs.org_id, chat_type=self.chat_type
        )

    def enrich_base_model(self, parsed_completion: ParserType) -> LiveQuestionExtractionSchema:
        self.inputs.question_extracted = parsed_completion.parsed_completion.get("answer")
        self.inputs.confidence = parsed_completion.parsed_completion.get("confidence")

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
                return OpenaiChat(ChatOpenaiGpt35()).predict(messages)
            except Exception as e:
                logger.error(f"Openai chat_completion error {e}", extra={"error": e})
                return AnthropicChat(ChatAnthropicClaude3Haiku()).predict(messages)
        except Exception as e:
            logger.error(f"Anthropic chat_completion error {e}", extra={"error": e})
            return CohereChat(ChatCohereCommandLightNightly()).predict(messages)

    def parse_completion(self, completion: str) -> ParserType:
        return JsonParser.parse(text=completion)

    def predict(self, text: str, **kwargs) -> LiveQuestionExtractionSchema:
        message_system = self.fill_string(
            SYSTEM_MSG, [("$ORG_NAME", self.org), ("$DEAL_NAME", self.deal), ("$EXAMPLES", EXAMPLE)]
        )
        self.system_prompt_len = self.tokenizer.length_function(message_system)
        message_user = self.fill_string(USER_MSG, [("$INPUT", self.trim_context(text))])
        prediction = self.run_thread(message_user=message_user, message_system=message_system, last_n_messages=2)

        return prediction

    def store_to_db_base_model(self, input: LiveQuestionExtractionSchema) -> LiveQuestionExtractionSchema:
        return LiveQuestionExtractionRepository(self.db_session).create(input)


if __name__ == "__main__":
    from src.schemas import DealSchema, BotSchema, OrgSchema
    from src.repositories import BotRepository, OrgRepository, DealRepository
    from src.db.db import get_session

    inputs = LiveQuestionExtractionSchema(
        bot_id="153585b1-883a-5cc9-a443-510b99764841",
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
    db_bot = BotRepository(db_session).read(inputs.bot_id)
    if not db_bot:
        db_bot = BotRepository(db_session).create(BotSchema(id=inputs.bot_id, deal_id=db_deal.id, org_id=db_org.id))
    LiveQuestionExtraction(db_session, inputs).predict(INPUT)
