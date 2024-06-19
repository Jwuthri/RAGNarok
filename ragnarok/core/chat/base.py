from abc import ABC, abstractmethod
from typing import Optional, Any

from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.prompt import PromptSchema


class ChatManager(ABC):
    @abstractmethod
    def complete(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        ...

    @abstractmethod
    async def a_complete(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        ...

    @abstractmethod
    def describe_models(self):
        ...

    @abstractmethod
    def format_message(self, messages: list[ChatMessageSchema]) -> Any:
        ...

    def predict(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        completion: PromptSchema = self.complete(messages, response_format, stream, tools)

        return completion

    async def a_predict(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        completion: PromptSchema = await self.a_complete(messages, response_format, stream, tools)

        return completion
