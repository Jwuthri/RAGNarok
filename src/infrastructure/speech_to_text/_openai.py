import logging

from src.infrastructure.speech_to_text.base import SpeechToTextManager


logger = logging.getLogger(__name__)


class OpenaiSpeechToText(SpeechToTextManager):
    ...
