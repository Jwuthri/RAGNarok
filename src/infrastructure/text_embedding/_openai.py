import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager
from src import API_KEYS
from src.utils.markdown_utils import align_markdown_table

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

    def embed_str(self, string: str) -> Embedding_typing:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.client.embeddings.create(input=[string], model=self.model_name).data.embedding

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | MODEL                    | ~ PAGES PER DOLLAR  | PERFORMANCE ON MTEB EVAL | MAX INPUT |
            |--------------------------|---------------------|--------------------------|-----------|
            | text-embedding-3-small   | 62,500              | 62.3%                    | 8191      |
            | text-embedding-3-large   | 9,615               | 64.6%                    | 8191      |
            | text-embedding-ada-002   | 12,500              | 61.0%                    | 8191      |
            """
            )
        )


if __name__ == "__main__":
    x = OpenaiEmbedding()
    x.describe_models()
