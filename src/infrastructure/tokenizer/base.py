from abc import ABC


class TokenizerManager(ABC):
    @classmethod
    def tokenize(self, text: str):
        return text.split()

    @classmethod
    def number_tokens(self, text: str):
        return len(self.tokenize(text))
