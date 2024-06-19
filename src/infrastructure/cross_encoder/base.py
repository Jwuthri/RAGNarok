from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class Texts(BaseModel):
    texts: tuple[str, str]


class CrossEncoderType(BaseModel):
    cost: Optional[float] = None
    latency: Optional[float] = None
    texts: Texts
    score: float


class TextCrossEncoderManager(ABC):
    @abstractmethod
    def encode(self, batch: list[Texts]) -> CrossEncoderType:
        ...

    @abstractmethod
    def describe_models(self):
        ...
