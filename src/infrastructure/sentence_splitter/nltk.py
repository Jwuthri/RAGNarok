import logging

from src.infrastructure.sentence_splitter.base import SentenceSplitterManager

logger = logging.getLogger(__name__)


class NltkSentenceSplitter(SentenceSplitterManager):
    def split_sequence(self, text: str) -> list[str]:
        try:
            from nltk.tokenize import sent_tokenize
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install nltk`")

        return sent_tokenize(text)

    def split_sequences(self, texts: list[str]) -> list[str]:
        sentences = [self.split_sequence(text) for text in texts]

        return sum(sentences, [])  # noqa
