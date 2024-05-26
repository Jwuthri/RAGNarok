from abc import abstractmethod, ABC
from typing import Optional
import logging

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.infrastructure.tokenizer.base import TokenizerManager
from src.infrastructure.completion_parser.base import ParserType
from src.schemas import ChatMessageSchema, PromptSchema, ChatSchema
from src.repositories.discovery_question import DiscoveryQuestionRepository
from src.repositories import (
    ChatRepository,
    OrgRepository,
    UserRepository,
    PromptRepository,
    BotRepository,
    DealRepository,
    ChatMessageRepository,
)

logger = logging.getLogger(__name__)


class BaseCore(ABC):
    def __init__(self, db_session: Session, application: str) -> None:
        self.db_session = db_session
        self.chat_type = application
        self.discovery_question = None
        self.tokenizer = TokenizerManager()
        self.inputs = None
        self.deal = None
        self.user = None
        self.org = None
        self.bot = None
        self.system_prompt_len = 0

    @abstractmethod
    def enrich_base_model(self, parsed_completion: ParserType) -> BaseModel:
        ...

    @abstractmethod
    def is_correct_prediction(self, parsed_completion: ParserType) -> bool:
        ...

    @abstractmethod
    def chat_completion(self, messages: list[ChatMessageSchema]) -> PromptSchema:
        ...

    @abstractmethod
    def parse_completion(self, completion: str) -> ParserType:
        ...

    @abstractmethod
    def store_to_db_base_model(self, input: BaseModel) -> BaseModel:
        ...

    @abstractmethod
    def build_chat(self) -> ChatSchema:
        ...

    @abstractmethod
    def trim_context(self, text: str) -> str:
        ...

    def run_thread(
        self, message_user: str, message_system: str, last_n_messages: int, **kwargs
    ) -> BaseModel | list[BaseModel]:
        history = self.fetch_history_messages(last_n_messages=last_n_messages, message=message_system)
        assert self.system_prompt_len > 0, "The system prompt is not setup!"
        user_message = self.get_user_message(chat_id=history[0].chat_id, message=message_user)
        chat_completion = self.chat_completion(history + [user_message])
        assistant_message = self.get_assistant_message(chat_completion, chat_id=history[0].chat_id)
        user_message.prompt_id = chat_completion.id
        if hasattr(self.inputs, "prompt_id"):
            self.inputs.prompt_id = chat_completion.id

        PromptRepository(self.db_session).create(data=chat_completion)
        ChatMessageRepository(self.db_session).create(data=user_message)
        ChatMessageRepository(self.db_session).create(data=assistant_message)
        parsed_completion = self.parse_completion(completion=chat_completion.prediction)
        if not parsed_completion.parsed_completion:
            logger.debug(f"parsed_completion empty: {parsed_completion}")
            return self.inputs
        if not self.is_correct_prediction(parsed_completion):
            logger.debug(f"incorrect parsed_completion: {parsed_completion}")
            return self.inputs
        logger.debug(f"enriching input with {parsed_completion}")

        return self.store_to_db_base_model(self.enrich_base_model(parsed_completion))

    def fill_string(self, string: str, source_target: list[tuple[str, str]]) -> str:
        for source, target in source_target:
            string = string.replace(source, target or "")

        return string

    def fetch_info(self):
        if hasattr(self.inputs, "bot_id") and self.inputs.bot_id:
            bot_id = self.inputs.bot_id
            db_bot = BotRepository(self.db_session).read(bot_id)
            if not db_bot:
                raise Exception(f"Bot:{bot_id} is missing")
            self.bot = db_bot.id

        if hasattr(self.inputs, "user_id") and self.inputs.user_id:
            user_id = self.inputs.user_id
            db_user = UserRepository(self.db_session).read(user_id)
            if not db_user:
                raise Exception(f"User:{user_id} is missing")
            self.user = db_user.name

        if hasattr(self.inputs, "deal_id") and self.inputs.deal_id:
            deal_id = self.inputs.deal_id
            db_deal = DealRepository(self.db_session).read(deal_id)
            if not db_deal:
                raise Exception(f"Deal:{deal_id} is missing")
            self.deal = db_deal.name

        if hasattr(self.inputs, "org_id") and self.inputs.org_id:
            org_id = self.inputs.org_id
            db_org = OrgRepository(self.db_session).read(org_id)
            if not db_org:
                raise Exception(f"Org:{org_id} is missing")
            self.org = db_org.name

        if hasattr(self.inputs, "discovery_question_id") and self.inputs.discovery_question_id:
            discovery_question_id = self.inputs.discovery_question_id
            db_discovery_question = DiscoveryQuestionRepository(self.db_session).read(discovery_question_id)
            if not db_discovery_question:
                raise Exception(f"DiscoveryQuestion:{discovery_question_id} is missing")
            self.discovery_question = db_discovery_question.question

    def fetch_history_messages(
        self, last_n_messages: int, message: Optional[str] = None, **kwargs
    ) -> list[ChatMessageSchema]:
        last_n_messages += 1 if last_n_messages % 2 != 0 and last_n_messages != 0 else last_n_messages
        chat = self.build_chat()
        db_chat = ChatRepository(self.db_session).read(chat.id)
        if not db_chat:
            logger.debug(f"chat created: {chat.id}")
            db_chat = ChatRepository(self.db_session).create(chat)

        history = ChatMessageRepository(self.db_session).read_chat(chat_id=chat.id, last_n_messages=last_n_messages)
        if not history:
            system = self.get_system_message(chat_id=chat.id, message=message)
            history = [ChatMessageRepository(self.db_session).create(data=system)]

        return history

    def get_system_message(self, chat_id: str, message: str, **kwargs) -> ChatMessageSchema:
        message = ChatMessageSchema(role="system", message=message, prompt_id=None, chat_id=chat_id)
        logger.debug(f"system_message created: {message}")

        return message

    def get_user_message(self, chat_id: str, message: str, **kwargs) -> ChatMessageSchema:
        message = ChatMessageSchema(role="user", message=message, prompt_id=None, chat_id=chat_id)
        logger.debug(f"user_message created: {message}")

        return message

    def get_assistant_message(self, completion: PromptSchema, chat_id: str, **kwargs) -> ChatMessageSchema:
        message = ChatMessageSchema(
            role="assistant", message=completion.prediction, prompt_id=completion.id, chat_id=chat_id
        )
        logger.debug(f"assistant_message created: {message}")

        return message
