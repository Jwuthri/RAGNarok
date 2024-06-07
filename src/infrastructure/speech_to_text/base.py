from abc import ABC, abstractmethod
from pathlib import Path


class SpeechToTextManager(ABC):
    @abstractmethod
    def describe_models(self):
        ...
