import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.repositories import DealKnowledgeExtractionRepository
from src.infrastructure.completion_parser import ParserType, JsonParser
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.prompts.deal_knowledge_extraction import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT
from src.schemas import ChatMessageSchema, PromptSchema, AskAboutSchema
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly

logger = logging.getLogger(__name__)


class AskAboutDeal(BaseCore):
    def __init__(self, db_session: Session, inputs: AskAboutSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.ask_about_deal.value)
        self.inputs = inputs
        self.set_company_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt35())

    def trim_context(self, text: str) -> str:
        max_user_message_len = (
            ChatOpenaiGpt35().context_size - self.system_prompt_len - ChatOpenaiGpt35().max_output
        ) // 2

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
        input.answer = parsed_completion.parsed_completion

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

    def predict(self, text: str) -> DealDiscoveryQuestionSchema:
        message_system = self.fill_string(
            SYSTEM_MSG,
            [
                ("$ORG_NAME", self.org),
                ("$DEAL_NAME", self.deal),
                ("$EXAMPLES", EXAMPLE),
                ("$DISCOVERY_QUESTION", self.discovery_question),
            ],
        )
        message_user = self.fill_string(USER_MSG, [("$INPUT", text)])
        prediction = self.run_thread(
            message_system=message_system, message_user=message_user, last_n_messages=2, text=text
        )

        return prediction

    def store_to_db_base_model(self, input: list[DealDiscoveryQuestionSchema]) -> list[DealDiscoveryQuestionSchema]:
        return [DealDiscoveryQuestionRepository(self.db_session).create(x) for x in input]
