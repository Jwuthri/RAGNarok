from abc import ABC, abstractmethod
from typing import Optional

from src.db.db import get_session
from src.repositories.prompt import PromptRepository
from src.schemas.chat_message import ChatMessage
from src.schemas.prompt import PromptSchema

Chat_typing = PromptSchema


class ChatManager(ABC):
    @abstractmethod
    def complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        ...

    @abstractmethod
    async def a_complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        ...

    @abstractmethod
    def describe_models(self):
        ...

    def to_db(self, completion: Chat_typing):
        db = get_session()

        return PromptRepository(db).create(data=completion)

    def predict(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        to_db: Optional[bool] = True,
    ) -> Chat_typing:
        completion: Chat_typing = self.complete(messages, response_format, stream)
        self.to_db(completion) if to_db else None

        return completion

    async def a_predict(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        to_db: Optional[bool] = True,
    ) -> Chat_typing:
        completion: Chat_typing = await self.a_complete(messages, response_format, stream)
        self.to_db(completion) if to_db else None

        return completion
