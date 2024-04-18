import logging

from sqlalchemy.orm import Session

from src.repositories import (
    ChatRepository,
    OrgRepository,
    UserRepository,
    PromptRepository,
    ChatMessageRepository,
    FollowUpEmailGenerationRepository,
)
from src.schemas import ChatMessageSchema, ChatOpenaiGpt35, PromptSchema, ChatSchema, FollowUpEmailGenerationSchema
from src.prompts.followup_email_generation import SYSTEM_MSG, USER_MSG, EXAMPLE
from src.infrastructure.completion_parser import StringParser
from src.infrastructure.chat import OpenaiChat
from src.core import Applications

logger = logging.getLogger(__name__)


class FollowUpEmailGeneration:
    def __init__(self, db_session: Session, inputs: FollowUpEmailGenerationSchema) -> None:
        self.db_session = db_session
        self.inputs = inputs

    def predict(self, **kwargs):
        history = self.fetch_history_messages(last_n_messages=2)
        user_message = self.get_user_message(chat_id=history[0].chat_id)
        completion = OpenaiChat(ChatOpenaiGpt35()).predict(history + [user_message])
        assistant_message = self.get_assistant_message(completion, chat_id=history[0].chat_id)
        user_message.prompt_id = completion.id
        PromptRepository(self.db_session).create(data=completion)
        ChatMessageRepository(self.db_session).create(data=user_message)
        ChatMessageRepository(self.db_session).create(data=assistant_message)
        parsed_completion = StringParser.parse(text=completion.prediction)
        if not parsed_completion.parsed_completion:
            return self.inputs

        if not self.is_correct_prediction(parsed_completion.parsed_completion):
            return self.inputs

        self.inputs.generated_email = parsed_completion.parsed_completion
        FollowUpEmailGenerationRepository(self.db_session).create(self.inputs)

        return self.inputs

    def is_correct_prediction(self, prediction: str):
        return not bool("idk" in prediction)

    def fetch_history_messages(self, last_n_messages: int, **kwargs) -> list[ChatMessageSchema]:
        last_n_messages += 1 if last_n_messages % 2 != 0 else last_n_messages

        db_org = OrgRepository(self.db_session).read(self.inputs.org_id)
        if not db_org:
            raise Exception(f"Org:{self.inputs.org_id} is missing")

        db_user = UserRepository(self.db_session).read(self.inputs.user_id)
        if not db_user:
            raise Exception(f"User:{self.inputs.user_id} is missing")

        chat = ChatSchema(user_id=self.inputs.user_id, chat_type=Applications.followup_email_generation.value)
        db_chat = ChatRepository(self.db_session).read(chat.id)
        if not db_chat:
            db_chat = ChatRepository(self.db_session).create(chat)

        history = ChatMessageRepository(self.db_session).read_chat(chat_id=chat.id, last_n_messages=last_n_messages)
        if not history:
            text = SYSTEM_MSG
            replacements = [
                ("$ORG_NAME", db_org.name),
                ("$EXAMPLES", EXAMPLE),
            ]
            for old, new in replacements:
                text = text.replace(old, new)
            system = ChatMessageSchema(role="system", message=text, chat_id=chat.id)
            ChatMessageRepository(self.db_session).create(data=system)

            return [system]

        return history

    def get_user_message(self, chat_id: str, **kwargs):
        return ChatMessageSchema(
            role="user",
            message=USER_MSG.replace("$INPUT", str(self.inputs.highlights)),
            chat_id=chat_id,
        )

    def get_assistant_message(self, completion: PromptSchema, chat_id: str, **kwargs):
        return ChatMessageSchema(
            role="assistant", message=completion.prediction, prompt_id=completion.id, chat_id=chat_id
        )


if __name__ == "__main__":
    from src.schemas.followup_email_generation import Hightlight, URN
    from src.schemas import OrgSchema, UserSchema
    from src.db.db import get_session

    inputs = FollowUpEmailGenerationSchema(
        org_id="383a829a-9fe4-5368-8d6f-254530c37242",
        user_id="a689a31e-e63c-532c-9631-ebd39b9c5534",
        creator_type="simulation",
        highlights=[
            Hightlight(
                highlight="Split's is a unique SDK architecture ensures that sensitive customer data is processed locally",
                urn=URN(type="", id="", name="", url=""),
                urn_summary=None,
                question="What is split?",
                summary="Split's is unique SDK architecture ensures that sensitive customer data.",
            ),
            Hightlight(
                highlight=None,
                urn=URN(
                    type="case_studies",
                    name="Eventbrite – Customers – Split",
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
