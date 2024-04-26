import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.core.base import BaseCore
from src.repositories import OrgRepository, UserRepository
from src.infrastructure.completion_parser import StringParser
from src.infrastructure.completion_parser.base import ParserType
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.prompts.followup_email_generation import SYSTEM_MSG, USER_MSG, EXAMPLE
from src.repositories.followup_email_generation import FollowUpEmailGenerationRepository
from src.schemas.chat import ChatSchema
from src.schemas.models import ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly
from src.schemas import ChatMessageSchema, ChatOpenaiGpt35, PromptSchema, FollowUpEmailGenerationSchema

logger = logging.getLogger(__name__)


class FollowUpEmailGeneration(BaseCore):
    def __init__(self, db_session: Session, inputs: FollowUpEmailGenerationSchema) -> None:
        super().__init__(db_session=db_session, application=Applications.followup_email_generation.value)
        self.inputs = inputs
        self.set_company_info()

    def build_chat(self) -> ChatSchema:
        return ChatSchema(user_id=self.inputs.user_id, org_id=self.inputs.org_id, chat_type=self.chat_type)

    def predict(self) -> FollowUpEmailGenerationSchema:
        message_system = self.fill_string(
            SYSTEM_MSG, [("$ORG_NAME", self.org), ("$DEAL_NAME", self.deal), ("$EXAMPLES", EXAMPLE)]
        )
        message_user = self.fill_string(USER_MSG, [("$INPUT", str(self.inputs.highlights))])
        prediction = self.run_thread(message_user=message_user, message_system=message_system, last_n_messages=0)

        return prediction

    def is_correct_prediction(self, parsed_completion: ParserType) -> bool:
        return not bool("idk" in parsed_completion.parsed_completion)

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
        return StringParser.parse(text=completion)

    def enrich_base_model(self, parsed_completion: ParserType) -> FollowUpEmailGenerationSchema:
        input = self.inputs.model_copy()
        input.generated_email = parsed_completion.parsed_completion

        return input

    def store_to_db_base_model(self, input: FollowUpEmailGenerationSchema) -> FollowUpEmailGenerationSchema:
        return FollowUpEmailGenerationRepository(self.db_session).create(input)


if __name__ == "__main__":
    from src.schemas.followup_email_generation import Hightlight, URNSchema
    from src.schemas import OrgSchema, UserSchema
    from src.db.db import get_session

    inputs = FollowUpEmailGenerationSchema(
        org_id="383a829a-9fe4-5368-8d6f-254530c37242",
        user_id="a689a31e-e63c-532c-9631-ebd39b9c5534",
        creator_type="simulation",
        highlights=[
            Hightlight(
                highlight="Split's is a unique SDK architecture ensures that sensitive customer data is processed locally",
                urn=URNSchema(type="", id="", name="", url=""),
                urn_summary=None,
                question="What is split?",
                summary="Split's is unique SDK architecture ensures that sensitive customer data.",
            ),
            Hightlight(
                highlight=None,
                urn=URNSchema(
                    type="case_studies",
                    name="Eventbrite Customers – Split",
                    id="Eventbrite – Customers – Split",
                    url="https://www.split.io/customers/eventbrite/",
                ),
                urn_summary="Eventbrite: A global ticketing and event technology platform.",
                question="What is split?",
                summary="Split's is unique SDK architecture ensures that sensitive customer data.",
            ),
        ],
    )
    db_session = get_session()
    db_org = OrgRepository(db_session).read(inputs.org_id)
    if not db_org:
        db_org = OrgRepository(db_session).create(OrgSchema(name="org_name", status="active", creator_type="user"))

    db_user = UserRepository(db_session).read(inputs.user_id)
    if not db_user:
        db_user = UserRepository(db_session).create(UserSchema(name="user", email="user@gmail.com"))

    FollowUpEmailGeneration(db_session, inputs).predict()
