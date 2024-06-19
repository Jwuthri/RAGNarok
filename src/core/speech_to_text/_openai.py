import logging
import time
from typing import Optional
from pathlib import Path

from src.core.speech_to_text.base import STTType, Segment, SpeechToTextManager
from src.schemas.models import STTModel, STTOpenaiBase, openai_stt_table
from src import console

logger = logging.getLogger(__name__)


class OpenaiSpeechToText(SpeechToTextManager):
    def __init__(self, model: STTModel, sync: Optional[bool] = True) -> None:
        self.model = model
        try:
            import whisper

            self.client = whisper.load_model(model.name)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai-whisper`")

    def speech_to_text(self, path: str | Path) -> STTType:
        t0 = time.perf_counter()
        result = self.client.transcribe(path)
        segments = [Segment(start=x["start"], end=x["end"], text=x["text"]) for x in result["segments"]]

        return STTType(
            file_path=path,
            language=result["language"],
            segments=segments,
            transcription=result["text"],
            latency=time.perf_counter() - t0,
            cost=self.model.cost_char * len(result["text"]),
        )

    @classmethod
    def describe_models(self):
        console.print(openai_stt_table)


if __name__ == "__main__":
    OpenaiSpeechToText.describe_models()
    res = OpenaiSpeechToText(STTOpenaiBase()).speech_to_text(
        "/Users/julienwuthrich/GitHub/RAGNarok/data/processed/tts/test.mp3"
    )
    logger.info(res)
