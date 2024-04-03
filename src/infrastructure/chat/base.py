from abc import ABC, abstractmethod

from src.db.db import get_session
from src.repositories.prompt import PromptRepository
from src.schemas.prompt import PromptSchema

Chat_typing = PromptSchema


class ChatManager(ABC):
    @abstractmethod
    def complete(self, messages: list[dict[str, str]], stream: bool) -> PromptSchema:
        ...

    @abstractmethod
    def describe_models(self):
        ...

    def predict(self, messages: list[dict[str, str]], stream: bool, to_db: bool = True) -> PromptSchema:
        completion: PromptSchema = self.complete(messages, stream)
        if to_db:
            db = get_session()
            _ = PromptRepository(db).create(data=completion)

        return completion
