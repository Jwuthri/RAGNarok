import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager
from src import API_KEYS

logger = logging.getLogger(__name__)


class OpenaiEmbedding(TextEmbeddingManager):
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=API_KEYS.OPENAI_API_KEY)
            self.info_model = {"dimension": 1536, "max_seq_length": 8192}
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def embed_batch(self, batch: list[str]) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.client.embeddings.create(input=batch, model=self.model_name).data[0].embedding

    def embed_query(self, query: str) -> Embedding_typing:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.client.embeddings.create(input=[query], model=self.model_name).data.embedding
