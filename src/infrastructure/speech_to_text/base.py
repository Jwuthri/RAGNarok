from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class Segment(BaseModel):
    start: float
    end: float
    text: str


class STTType(BaseModel):
    file_path: str
    transcription: str
    segments: list[Segment]
    language: Optional[str] = None
    latency: Optional[float] = None
    cost: Optional[float] = None


class SpeechToTextManager(ABC):
    def speech_to_text(self, path: str | Path) -> STTType:
        ...

    @abstractmethod
    def describe_models(self):
        ...
