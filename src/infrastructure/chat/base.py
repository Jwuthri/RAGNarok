from abc import ABC, abstractmethod
from typing import Any

Chat_typing = dict[str, Any]


class ChatManager(ABC):
    @abstractmethod
    def complete(self, system: str, message: str, stream: bool):
        ...

    @abstractmethod
    def describe_models(self):
        ...
