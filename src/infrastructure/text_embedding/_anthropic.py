import logging

from src.infrastructure.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from src import Table, CONSOLE, API_KEYS
from src.schemas.models import EmbeddingAnthropicVoyage2, EmbeddingModel

logger = logging.getLogger(__name__)


class AnthropicEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            import voyageai

            self.client = voyageai.Client(API_KEYS.VOYAGE_AI_API_KEY)
            self.info_model = {"dimension": self.model.dimension, "max_seq_length": self.model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install voyageai`")

    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[EmbeddingType]:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of the input strings.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return [
            EmbeddingType(text=batch[i], embedding=x)
            for i, x in enumerate(self.client.embed(batch, model=self.model.name, input_type=input_type).embeddings)
        ]

    def embed_str(self, string: str, input_type: InputType = None) -> EmbeddingType:
        """
        This function takes a string query as input and returns a list of float embeddings using a
        pre-trained model.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return [
            EmbeddingType(text=string, embedding=x)
            for i, x in enumerate(self.client.embed([string], model=self.model.name, input_type=input_type).embeddings)
        ][0]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model", justify="left")
        table.add_column("Context Length", justify="left")
        table.add_column("Embedding Dimension", justify="left")
        table.add_column("Description", justify="left")

        table.add_row("voyage-large-2", "16000", "1536", "Voyage AI's most powerful generalist embedding model.")
        table.add_row(
            "voyage-code-2",
            "16000",
            "1536",
            "Optimized for code retrieval (17% better than alternatives), and also SoTA on general-purpose corpora. See this Voyage blog post for details.",
        )
        table.add_row(
            "voyage-2", "4000", "1024", "Base generalist embedding model optimized for both latency and quality."
        )
        table.add_row(
            "voyage-lite-02-instruct",
            "4000",
            "1024",
            "Instruction-tuned for classification, clustering, and sentence textual similarity tasks, which are the only recommended use cases for this model.",
        )

        CONSOLE.print(table)


if __name__ == "__main__":
    AnthropicEmbedding.describe_models()
    AnthropicEmbedding.describe_input()
    res = AnthropicEmbedding(EmbeddingAnthropicVoyage2()).embed_str("where is it?", input_type="query")
    logger.info(res)
