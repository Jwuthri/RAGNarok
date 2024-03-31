import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager
from src import API_KEYS
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class CohereEmbedding(TextEmbeddingManager):
    def __init__(self, model_name: str = "embed-english-v3.0"):
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.OPENAI_API_KEY)
            self.info_model = {"dimension": 1024, "max_seq_length": 512}
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
        return self.client.embed(input=batch, model=self.model_name, input_type=input_type)

    def embed_str(self, string: str, input_type: str) -> Embedding_typing:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.client.embed(input=[string], model=self.model_name, input_type=input_type)[0]

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | LATEST MODEL                    | DESCRIPTION                                                                                          | DIMENSIONS | MAX TOKENS (CONTEXT LENGTH) | SIMILARITY METRIC      | ENDPOINTS        |
            |---------------------------------|------------------------------------------------------------------------------------------------------|------------|-----------------------------|------------------------|------------------|
            | embed-multilingual-v3.0         | Provides multilingual classification and embedding support. See supported languages here.            | 1024       | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-multilingual-light-v3.0   | A smaller, faster version of embed-multilingual-v3.0. Almost as capable, but a lot faster.           | 384        | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-multilingual-v2.0         | Provides multilingual classification and embedding support. See supported languages here.            | 768        | 256                         | Dot Product Similarity | Classify, Embed  |
            | embed-english-v3.0              | A model that allows for text to be classified or turned into embeddings. English only.               | 1024       | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-english-light-v3.0        | A smaller, faster version of embed-english-v3.0. Almost as capable, but a lot faster. English only.  | 384        | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-english-v2.0              | Our older embeddings model that allows for text to be classified or turned into embeddings. English  | 4096       | 512                         | Cosine Similarity      | Classify, Embed  |
            | embed-english-light-v2.0        | A smaller, faster version of embed-english-v2.0. Almost as capable, but a lot faster. English only.  | 1024       | 512                         | Cosine Similarity      | Classify, Embed  |
            """
            )
        )


if __name__ == "__main__":
    CohereEmbedding.describe_models()
