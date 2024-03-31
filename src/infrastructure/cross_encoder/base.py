from abc import ABC, abstractmethod

CrossEncoder_typing = list[float]


class TextCrossEncoderManager(ABC):
    @abstractmethod
    def encode(self, batch: list[tuple[str, str]]) -> CrossEncoder_typing:
        ...

    @abstractmethod
    def describe_models(self):
        ...
