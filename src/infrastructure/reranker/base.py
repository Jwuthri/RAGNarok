from abc import ABC, abstractmethod
from typing import Any

Rerank_typing = dict[str, Any]


class TextRerankerManager(ABC):
    @abstractmethod
    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> Rerank_typing:
        """
        This is a Python function that takes a list of strings as input and returns a list of lists of
        floats as output.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        """
        ...
