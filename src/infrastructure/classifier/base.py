from abc import ABC, abstractmethod
from typing import Any

Classifier_typing = dict[str, Any]


class ClassifierManager(ABC):
    @abstractmethod
    def classify(self, examples: list[tuple[str, str]], inputs: list[str]) -> Classifier_typing:
        ...
