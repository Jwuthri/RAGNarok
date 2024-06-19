import logging
import time

from ragnarok import console, API_KEYS
from ragnarok.core.tokenizer import AnthropicTokenizer
from ragnarok.core.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from ragnarok.schemas.models import EmbeddingAnthropicVoyage2, EmbeddingModel, anthropic_embedding_table

logger = logging.getLogger(__name__)


class AnthropicEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        self.tokenizer = AnthropicTokenizer(model)
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
        t0 = time.perf_counter()

        return [
            EmbeddingType(
                text=batch[i],
                embedding=x,
                cost=self.model.cost_token * self.tokenizer.length_function(batch[i]),
                latency=time.perf_counter() - t0,
            )
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
        t0 = time.perf_counter()

        return [
            EmbeddingType(
                text=string,
                embedding=x,
                cost=self.model.cost_token * self.tokenizer.length_function(string),
                latency=time.perf_counter() - t0,
            )
            for i, x in enumerate(self.client.embed([string], model=self.model.name, input_type=input_type).embeddings)
        ][0]

    @classmethod
    def describe_models(self):
        console.print(anthropic_embedding_table)


if __name__ == "__main__":
    AnthropicEmbedding.describe_models()
    AnthropicEmbedding.describe_input()
    res = AnthropicEmbedding(EmbeddingAnthropicVoyage2()).embed_str("where is it?", input_type="query")
    logger.info(res)
