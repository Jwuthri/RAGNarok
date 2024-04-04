import logging
from typing import Literal

from src.infrastructure.text_embedding.base import Embedding, EmbeddingManager, InputType
from src import Table, CONSOLE, API_KEYS
from src.schemas.models import EmbeddingModel, EmbeddingOpenaiSmall3

logger = logging.getLogger(__name__)


class OpenaiEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=API_KEYS.OPENAI_API_KEY)
            self.info_model = {"dimension": self.model.dimension, "max_seq_length": self.model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[Embedding]:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return [
            Embedding(text=batch[i], embedding=x.embedding)
            for i, x in enumerate(self.client.embeddings.create(input=batch, model=self.model.name).data)
        ]

    def embed_str(self, string: str, input_type: InputType = None) -> Embedding:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return [
            Embedding(text=string, embedding=x.embedding)
            for i, x in enumerate(self.client.embeddings.create(input=[string], model=self.model.name).data)
        ]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("MODEL", justify="left")
        table.add_column("PAGES PER DOLLAR", justify="left")
        table.add_column("PERFORMANCE ON MTEB EVAL", justify="left")
        table.add_column("MAX INPUT", justify="left")

        table.add_row("text-embedding-3-small", "62,500", "62.3%", "8191")
        table.add_row("text-embedding-3-large", "9,615", "64.6%", "8191")
        table.add_row("text-embedding-ada-002", "12,500", "61.0%", "8191")

        CONSOLE.print(table)


if __name__ == "__main__":
    OpenaiEmbedding.describe_models()
    OpenaiEmbedding.describe_models()
    res = OpenaiEmbedding(EmbeddingOpenaiSmall3()).embed_str("where is it?", input_type="search_query")
    logger.info(res)
