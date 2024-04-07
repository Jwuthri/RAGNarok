import logging

from src.infrastructure.sentence_splitter.base import SentenceSplitterManager

logger = logging.getLogger(__name__)


class NltkSentenceSplitter(SentenceSplitterManager):
    def __init__(self) -> None:
        try:
            from nltk.tokenize import sent_tokenize

            self.sent_tokenize = sent_tokenize
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install nltk`")

    def split_sequence(self, text: str) -> list[str]:
        return self.sent_tokenize(text)

    def split_sequences(self, texts: list[str]) -> list[str]:
        sentences = [self.split_sequence(text) for text in texts]

        return sum(sentences, [])
