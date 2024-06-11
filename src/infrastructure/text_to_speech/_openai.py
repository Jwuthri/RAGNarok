import logging
from pathlib import Path
from typing import Optional

from src import PROJECT_PATHS, Table, console, API_KEYS
from src.infrastructure.text_to_speech.base import TextToSpeechManager
from src.schemas.models import TTSModel, TTSOpenai1, openai_tts
from src.utils.decorator import a_timer_func, timer_func


logger = logging.getLogger(__name__)


class OpenaiTextToSpeech(TextToSpeechManager):
    def __init__(self, model: TTSModel, sync: Optional[bool] = True):
        self.model = model
        try:
            from openai import OpenAI, AsyncOpenAI

            if sync:
                self.client = OpenAI(api_key=API_KEYS.OPENAI_API_KEY)
            else:
                self.client = AsyncOpenAI(api_key=API_KEYS.OPENAI_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

    @timer_func
    def stream_text_to_speech(self, text: str, path: str | Path):
        with self.client.audio.speech.with_streaming_response.create(
            model=self.model.name,
            voice=self.model.voice,
            input=text,
        ) as response:
            response.stream_to_file(path)

    @a_timer_func
    async def a_stream_text_to_speech(self, text: str, path: str | Path):
        async with self.client.audio.speech.with_streaming_response.create(
            model=self.model.name, voice=self.model.voice, input=text
        ) as response:
            response.stream_to_file(path)

    @classmethod
    def describe_models(self):
        console.print(openai_tts)


if __name__ == "__main__":
    OpenaiTextToSpeech.describe_models()
    # tts = OpenaiTextToSpeech(TTSOpenai1(voice="alloy"))
    # tts.stream_text_to_speech(
    #     text="Hey! I'd like to set a meeting with your Sales manager. How can we proceed?",
    #     path=PROJECT_PATHS.PROCESSED_DATA / "tts" / "test.mp3",
    # )
