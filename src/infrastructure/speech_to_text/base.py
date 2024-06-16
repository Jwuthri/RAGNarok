from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel


class Segment(BaseModel):
    start: float
    end: float
    text: str


class STTType(BaseModel):
    file_path: str
    transcription: str
    segments: list[Segment]
    latency: float
    language: str


class SpeechToTextManager(ABC):
    def speech_to_text(self, path: str | Path) -> STTType:
        ...

    @abstractmethod
    def describe_models(self):
        ...
