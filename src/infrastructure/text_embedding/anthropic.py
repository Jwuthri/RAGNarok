import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager
from src import API_KEYS

logger = logging.getLogger(__name__)


class AnthropicEmbedding(TextEmbeddingManager):
    def __init__(self, model_name: str = "embed-english-v3.0"):
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client(API_KEYS.COHERE_API_KEY)
            self.info_model = {"dimension": 1536, "max_seq_length": 8192}
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def embed_batch(self, batch: list[str], input_type: str) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.client.embed(batch, model=self.model_name, input_type=input_type).embeddings[0]

    def embed_str(self, string: str, input_type: str) -> Embedding_typing:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.client.embed([string], model=self.model_name, input_type=input_type).embeddings[0]
