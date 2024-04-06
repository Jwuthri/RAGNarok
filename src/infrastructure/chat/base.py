from abc import ABC, abstractmethod
from typing import Optional, Any

from src.schemas.chat_message import ChatMessage
from src.schemas.prompt import PromptSchema

Chat_typing = PromptSchema


class ChatManager(ABC):
    @abstractmethod
    def complete(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> Chat_typing:
        ...

    @abstractmethod
    async def a_complete(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> Chat_typing:
        ...

    @abstractmethod
    def describe_models(self):
        ...

    @abstractmethod
    def format_message(self, messages: list[ChatMessage]) -> Any:
        ...

    def predict(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> Chat_typing:
        completion: Chat_typing = self.complete(messages, response_format, stream, tools)

        return completion

    async def a_predict(
        self,
        messages: list[ChatMessage],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> Chat_typing:
        completion: Chat_typing = await self.a_complete(messages, response_format, stream, tools)

        return completion
