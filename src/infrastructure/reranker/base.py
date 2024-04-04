from abc import ABC, abstractmethod

from pydantic import BaseModel


class RerankType(BaseModel):
    new_index: int
    previous_index: int
    score: float
    document: str


class RerankerManager(ABC):
    @abstractmethod
    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankType]:
        """
        This is a Python function that takes a list of strings as input and returns a list of lists of
        floats as output.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        """
        ...

    @abstractmethod
    def describe_models(self):
        ...
