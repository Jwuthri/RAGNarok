import logging
import time

from ragnarok.core.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from ragnarok.schemas.models import EmbeddingModel, MiniLML6v2, hf_embedding_table
from ragnarok import console

logger = logging.getLogger(__name__)


class SentenceTransformersEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            from sentence_transformers import SentenceTransformer

            self.client = SentenceTransformer(model.name)
            self.info_model = {"dimension": self.model.dimension, "max_seq_length": self.model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install sentence-transformers`")

    def embed_batch(self, batch: list[str], input_type: InputType = None) -> list[EmbeddingType]:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of each string in the input list.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        t0 = time.perf_counter()

        return [
            EmbeddingType(text=batch[i], embedding=x, cost=self.model.cost_token, latency=time.perf_counter() - t0)
            for i, x in enumerate(self.client.encode(batch, show_progress_bar=False).tolist())
        ]

    def embed_str(self, string: str, input_type: InputType = None) -> EmbeddingType:
        """
        This function takes a string query and returns its embedding as a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        t0 = time.perf_counter()

        return [
            EmbeddingType(text=string, embedding=x, cost=self.model.cost_token, latency=time.perf_counter() - t0)
            for i, x in enumerate(self.client.encode([string], show_progress_bar=False).tolist())
        ][0]

    @classmethod
    def describe_models(self):
        console.print(hf_embedding_table)


if __name__ == "__main__":
    SentenceTransformersEmbedding.describe_models()
    SentenceTransformersEmbedding.describe_input()
    res = SentenceTransformersEmbedding(MiniLML6v2()).embed_str("where is it?", input_type="search_query")
    logger.info(res)
