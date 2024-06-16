import logging

from src.infrastructure.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from src import console, API_KEYS
from src.schemas.models import EmbeddingModel, EmbeddingGoogle4, google_embedding_table

logger = logging.getLogger(__name__)


class GoogleEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            import google.generativeai as genai

            self.client = genai
            self.client.configure(api_key=API_KEYS.GOOGLE_API_KEY)
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install --upgrade google-cloud-aiplatform`")

    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[EmbeddingType]:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        ...

    def embed_str(self, string: str, input_type: InputType = None) -> EmbeddingType:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        ...

    @classmethod
    def describe_models(self):
        console.print(google_embedding_table)


if __name__ == "__main__":
    GoogleEmbedding.describe_models()
    res = GoogleEmbedding(EmbeddingGoogle4()).embed_str("where is it?", input_type="search_query")
    logger.info(res)
