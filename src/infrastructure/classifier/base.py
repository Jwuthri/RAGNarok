from abc import ABC, abstractmethod

from pydantic import BaseModel

Classifier_typing = list[str]


class Label(BaseModel):
    name: str
    description: str


class Example(BaseModel):
    text: str
    label: Label


class ClassifierManager(ABC):
    @abstractmethod
    def classify(self, labels: list[Label], inputs: list[str], examples: list[Example]) -> Classifier_typing:
        ...

    @abstractmethod
    def describe_models(self):
        ...
