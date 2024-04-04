import logging

from src.infrastructure.sentence_splitter.base import SentenceSplitterManager

logger = logging.getLogger(__name__)


class NltkSentenceSplitter(SentenceSplitterManager):
    def split_sequence(self, text: str) -> list[str]:
        """
        The function `split_sequence` uses NLTK's `sent_tokenize` to split a given text into a list of
        sentences.

        :param text: The `text` parameter in the `split_sequence` function is expected to be a string
        containing a sequence of text that you want to split into sentences. The function uses the NLTK
        library's `sent_tokenize` function to split the text into a list of sentences
        :type text: str
        :return: A list of strings containing the sentences extracted from the input text.
        """
        try:
            from nltk.tokenize import sent_tokenize
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install nltk`")

        return sent_tokenize(text)

    def split_sequences(self, texts: list[str]) -> list[str]:
        sentences = [self.split_sequence(text) for text in texts]

        return sum(sentences, [])
