from typing import Literal
from abc import ABC, abstractmethod

from pydantic import BaseModel

from src import Table, CONSOLE


class EmbeddingType(BaseModel):
    text: str
    embedding: list[float]


class InputType(BaseModel):
    value: Literal["query", "document"]


class EmbeddingManager(ABC):
    @abstractmethod
    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[EmbeddingType]:
        """
        This is a Python function that takes a list of strings as input and returns a list of lists of
        floats as output.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        """
        ...

    @abstractmethod
    def embed_str(self, string: str, input_type: InputType = None) -> EmbeddingType:
        """
        This function takes a string query as input and returns a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        """
        ...

    @abstractmethod
    def describe_models(self):
        ...

    @classmethod
    def describe_input(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Input Type", justify="left")
        table.add_column("Description", justify="left")

        table.add_row(
            "document", "Use this when you have texts (documents) that you want to store in a vector database."
        )
        table.add_row(
            "query",
            "Use this when structuring search queries to find the most relevant documents in your vector database.",
        )

        CONSOLE.print(table)
