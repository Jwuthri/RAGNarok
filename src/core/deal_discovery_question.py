import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.schemas.chat import ChatSchema
from src.infrastructure.tokenizer import OpenaiTokenizer
from src.repositories import DealDiscoveryQuestionRepository
from src.infrastructure.completion_parser import ParserType, JsonParser
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.schemas import ChatMessageSchema, PromptSchema, DealDiscoveryQuestionSchema
from src.prompts.deal_discovery_question import SYSTEM_MSG, USER_MSG, EXAMPLE, INPUT
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly

logger = logging.getLogger(__name__)


class DealDiscoveryQuestion(BaseCore):
    def __init__(self, db_session: Session, inputs: DealDiscoveryQuestionSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.deal_discovery_question.value)
        self.inputs = inputs
        self.set_company_info()
        self.tokenizer = OpenaiTokenizer(ChatOpenaiGpt35())

    def trim_context(self, text: str) -> str:
        max_user_message_len = (
            ChatOpenaiGpt35().context_size - self.system_prompt_len - ChatOpenaiGpt35().max_output
        ) // 2

        return self.tokenizer.get_last_n_tokens(text, n=max_user_message_len)

    def build_chat(self) -> ChatSchema:
        return ChatSchema(deal_id=self.inputs.deal_id, org_id=self.inputs.org_id, chat_type=self.chat_type)

    def enrich_base_model(self, parsed_completion: ParserType) -> DealDiscoveryQuestionSchema:
        input = self.inputs
        input.answer = parsed_completion.parsed_completion.get("answer")

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
                return OpenaiChat(ChatOpenaiGpt35()).predict(messages)
            except Exception as e:
                logger.error(f"Openai chat_completion error {e}", extra={"error": e})
                return AnthropicChat(ChatAnthropicClaude3Haiku()).predict(messages)
        except Exception as e:
            logger.error(f"Anthropic chat_completion error {e}", extra={"error": e})
            return CohereChat(ChatCohereCommandLightNightly()).predict(messages)

    def parse_completion(self, completion: str) -> ParserType:
        return JsonParser.parse(text=completion)

    def predict(self, text: str, **kwargs) -> DealDiscoveryQuestionSchema:
        message_system = self.fill_string(
            SYSTEM_MSG,
            [
                ("$ORG_NAME", self.org),
                ("$DEAL_NAME", self.deal),
                ("$EXAMPLES", EXAMPLE),
                ("$DISCOVERY_QUESTION", self.discovery_question),
            ],
        )
        self.system_prompt_len = self.tokenizer.length_function(message_system)
        message_user = self.fill_string(USER_MSG, [("$INPUT", self.trim_context(text))])
        prediction = self.run_thread(
            message_system=message_system, message_user=message_user, last_n_messages=2, text=text
        )

        return prediction

    def store_to_db_base_model(self, input: DealDiscoveryQuestionSchema) -> DealDiscoveryQuestionSchema:
        return DealDiscoveryQuestionRepository(self.db_session).update(_id=input.id, data=input)


if __name__ == "__main__":
    from src.repositories import DealRepository, OrgRepository, ProductRepository, DiscoveryQuestionRepository
    from src.schemas import DealSchema, OrgSchema, ProductSchema, DiscoveryQuestionSchema
    from src.db.db import get_session

    inputs = DealDiscoveryQuestionSchema(
        deal_id="91038e80-3b23-5ada-b684-04309119da20",
        org_id="383a829a-9fe4-5368-8d6f-254530c37242",
        discovery_question_id="901e1b51-5502-5de1-bf43-d343d30db409",
        product_id="676a3be6-5ca5-5a36-90b9-5c89065bf286",
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
    db_product = ProductRepository(db_session).read(inputs.product_id)
    if not db_product:
        db_product = ProductRepository(db_session).create(
            ProductSchema(name="product_name", org_id=db_org.id, default=True, creator_type="user")
        )
    db_discovery_question = DiscoveryQuestionRepository(db_session).read(inputs.discovery_question_id)
    if not db_discovery_question:
        db_discovery_question = DiscoveryQuestionRepository(db_session).create(
            DiscoveryQuestionSchema(question="what is your product?", org_id=db_org.id, product_id=db_product.id)
        )
    db_deal_discovery_question = DealDiscoveryQuestionRepository(db_session).read_by_discovery_question_id(
        inputs.discovery_question_id
    )
    if not db_deal_discovery_question:
        db_deal_discovery_question = DealDiscoveryQuestionRepository(db_session).create(
            DealDiscoveryQuestionSchema(
                deal_id=db_deal.id,
                org_id=db_org.id,
                discovery_question_id=db_discovery_question.id,
                product_id=db_product.id,
                answer=None,
            )
        )
    DealDiscoveryQuestion(db_session, inputs).predict(INPUT)
