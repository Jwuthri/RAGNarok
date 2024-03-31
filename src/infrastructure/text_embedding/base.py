import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
Embedding_typing = list[float]
Embeddings_typing = list[Embedding_typing]


class TextEmbeddingManager(ABC):
    @abstractmethod
    def embed_batch(self, batch: list[str]) -> Embeddings_typing:
        """
        This is a Python function that takes a list of strings as input and returns a list of lists of
        floats as output.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        """
        ...

    @abstractmethod
    def embed_str(self, string: str) -> Embedding_typing:
        """
        This function takes a string query as input and returns a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        """
        ...

    @abstractmethod
    def describe_models(self):
        ...
