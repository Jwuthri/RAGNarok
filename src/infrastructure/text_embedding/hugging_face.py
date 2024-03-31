import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager

logger = logging.getLogger(__name__)


class HuggingFaceEmbedding(TextEmbeddingManager):
    def __init__(self, model_name: str = "jinaai/jina-embeddings-v2-base-en"):
        try:
            from transformers import AutoModel

            self.embeddings = AutoModel.from_pretrained(model_name, trust_remote_code=True)
            self.info_model = {
                "dimension": self.embeddings.config.hidden_size,
                "max_seq_length": self.embeddings.config.max_position_embeddings,
            }
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def embed_batch(self, batch: list[str]) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of each string in the input list.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.embeddings.encode(batch).tolist()

    def embed_str(self, string: str) -> Embedding_typing:
        """
        This function takes a string query and returns its embedding as a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.embeddings.encode([string]).tolist()[0]
