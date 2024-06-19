from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class Label(BaseModel):
    name: str
    description: str


class Example(BaseModel):
    text: str
    label: Label


class ClassifierType(BaseModel):
    text: str
    label: str
    cost: Optional[float] = None
    latency: Optional[float] = None


class ClassifierManager(ABC):
    @abstractmethod
    def classify(self, labels: list[Label], inputs: list[str], examples: list[Example]) -> ClassifierType:
        ...

    @abstractmethod
    def describe_models(self):
        ...
