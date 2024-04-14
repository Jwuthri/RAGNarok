import logging

from sqlalchemy.orm import Session

from src.core import Applications
from src.prompts.live_question_extraction import SYSTEM_MSG, USER_MSG
from src.schemas.live_question_extraction import LiveQuestionSchema
from src.repositories.chat_message import ChatMessageRepository
from src.schemas.chat_message import ChatMessageSchema
from src.repositories.prompt import PromptRepository
from src.repositories.chat import ChatRepository
from src.repositories.bot import BotRepository
from src.infrastructure.chat import OpenaiChat
from src.schemas.models import ChatOpenaiGpt35
from src.schemas.prompt import PromptSchema
from src.schemas.chat import ChatSchema

logger = logging.getLogger(__name__)


class LiveQuestionExtraction:
    def __init__(self, db_session: Session, inputs: LiveQuestionSchema) -> None:
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

    def fetch_history_messages(self, last_n_messages: int, **kwargs) -> list[ChatMessageSchema]:
        last_n_messages += 1 if last_n_messages % 2 != 0 else last_n_messages
        db_bot = BotRepository(self.db_session).read(self.inputs.bot_id)
        if not db_bot:
            raise Exception(f"Bot:{self.inputs.bot_id} is missing")

        chat = ChatSchema(bot_id=self.inputs.bot_id, chat_type=Applications.live_question_extraction.value)
        db_chat = ChatRepository(self.db_session).read(chat.id)
        if not db_chat:
            db_chat = ChatRepository(self.db_session).create(chat)

        history = ChatMessageRepository(self.db_session).read_chat(chat_id=chat.id, last_n_messages=last_n_messages)
        if not history:
            text = SYSTEM_MSG
            replacements = [
                ("$ORG_NAME", self.inputs.org_id),
                ("$DEAL_NAME", self.inputs.deal_id),
                ("$EXAMPLES", "EXAMPLES"),
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
            message=USER_MSG.replace("$INPUT", "what is the best api for your product?"),
            chat_id=chat_id,
        )

    def get_assistant_message(self, completion: PromptSchema, chat_id: str, **kwargs):
        return ChatMessageSchema(
            role="assistant", message=completion.prediction, prompt_id=completion.id, chat_id=chat_id
        )


if __name__ == "__main__":
    from src.repositories import DealRepository, OrgRepository, BotRepository
    from src.schemas import DealSchema, BotSchema, OrgSchema
    from src.db.db import get_session

    inputs = LiveQuestionSchema(
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
    LiveQuestionExtraction(db_session, inputs).predict()
