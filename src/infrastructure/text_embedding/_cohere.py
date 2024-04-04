import logging

from src.infrastructure.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from src import Table, CONSOLE, API_KEYS
from src.schemas.models import EmbeddingCohereEnglishV3, EmbeddingModel

logger = logging.getLogger(__name__)


class CohereEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
            self.info_model = {"dimension": self.model.dimension, "max_seq_length": self.model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[EmbeddingType]:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        if input_type and input_type in ["query", "document"]:
            input_type = {"query": "search_query", "document": "search_document"}.get(input_type)

        return [
            EmbeddingType(text=batch[i], embedding=x)
            for i, x in enumerate(
                self.client.embed(texts=batch, model=self.model.name, input_type=input_type).embeddings
            )
        ]

    def embed_str(self, string: str, input_type: InputType = None) -> EmbeddingType:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        if input_type and input_type in ["query", "document"]:
            input_type = {"query": "search_query", "document": "search_document"}.get(input_type)

        return [
            EmbeddingType(text=string, embedding=x)
            for i, x in enumerate(
                self.client.embed(texts=[string], model=self.model.name, input_type=input_type).embeddings
            )
        ]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("LATEST MODEL", justify="left")
        table.add_column("DESCRIPTION", justify="left")
        table.add_column("DIMENSIONS", justify="left")
        table.add_column("MAX TOKENS (CONTEXT LENGTH)", justify="left")
        table.add_column("SIMILARITY METRIC", justify="left")
        table.add_column("ENDPOINTS", justify="left")

        table.add_row(
            "embed-multilingual-v3.0",
            "Provides multilingual classification and embedding support. See supported languages here.",
            "1024",
            "512",
            "Cosine Similarity",
            "Embed, Embed Jobs",
        )
        table.add_row(
            "embed-multilingual-light-v3.0",
            "A smaller, faster version of embed-multilingual-v3.0. Almost as capable, but a lot faster.",
            "384",
            "512",
            "Cosine Similarity",
            "Embed, Embed Jobs",
        )
        table.add_row(
            "embed-multilingual-v2.0",
            "Provides multilingual classification and embedding support. See supported languages here.",
            "768",
            "256",
            "Dot Product Similarity",
            "Classify, Embed",
        )
        table.add_row(
            "embed-english-v3.0",
            "A model that allows for text to be classified or turned into embeddings. English only.",
            "1024",
            "512",
            "Cosine Similarity",
            "Embed, Embed Jobs",
        )
        table.add_row(
            "embed-english-light-v3.0",
            "A smaller, faster version of embed-english-v3.0. Almost as capable, but a lot faster. English only.",
            "384",
            "512",
            "Cosine Similarity",
            "Embed, Embed Jobs",
        )
        table.add_row(
            "embed-english-v2.0",
            "Our older embeddings model that allows for text to be classified or turned into embeddings. English",
            "4096",
            "512",
            "Cosine Similarity",
            "Classify, Embed",
        )
        table.add_row(
            "embed-english-light-v2.0",
            "A smaller, faster version of embed-english-v2.0. Almost as capable, but a lot faster. English only.",
            "1024",
            "512",
            "Cosine Similarity",
            "Classify, Embed",
        )

        CONSOLE.print(table)


if __name__ == "__main__":
    CohereEmbedding.describe_models()
    CohereEmbedding.describe_input()
    res = CohereEmbedding(EmbeddingCohereEnglishV3()).embed_str("where is it?", input_type="query")
    logger.info(res)
