from abc import ABC

from src.schemas.models import ChatModel


class TokenizerManager(ABC):
    def __init__(self, model: ChatModel) -> None:
        self.model = model

    def encode(self, text: str):
        return text.split()

    def decode(self, tokens: list):
        return " ".join(tokens)

    def length_function(self, text: str):
        return len(self.encode(text))

    def get_last_n_tokens(self, text: str, n: int = None):
        n = -1 if not n or n < 0 else n

        return self.decode(self.encode(text)[-n:])
