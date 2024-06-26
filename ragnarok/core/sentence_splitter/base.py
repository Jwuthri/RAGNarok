from abc import ABC, abstractmethod


class SentenceSplitterManager(ABC):
    @abstractmethod
    def split_sequence(self, text: str) -> list[str]:
        ...

    def split_sequences(self, texts: list[str]) -> list[str]:
        ...
