from abc import ABC, abstractmethod
from pathlib import Path


class TextToSpeechManager(ABC):
    @abstractmethod
    def describe_models(self):
        ...

    @abstractmethod
    def stream_text_to_speech(self, text: str, path: str | Path):
        ...

    @abstractmethod
    async def a_stream_text_to_speech(self, text: str, path: str | Path):
        ...
