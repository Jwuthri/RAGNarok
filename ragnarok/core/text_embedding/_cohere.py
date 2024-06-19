import logging
import time

from ragnarok.core.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from ragnarok import console, API_KEYS
from ragnarok.schemas.models import EmbeddingCohereEnglishV3, EmbeddingModel, cohere_embedding_table
from ragnarok.core.tokenizer import CohereTokenizer

logger = logging.getLogger(__name__)


class CohereEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        self.tokenizer = CohereTokenizer(model)
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
        t0 = time.perf_counter()
        if input_type and input_type in ["query", "document"]:
            input_type = {"query": "search_query", "document": "search_document"}.get(input_type)

        return [
            EmbeddingType(
                text=batch[i],
                embedding=x,
                cost=self.model.cost_token * self.tokenizer.length_function(batch[i]),
                latency=time.perf_counter() - t0,
            )
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
        t0 = time.perf_counter()
        if input_type and input_type in ["query", "document"]:
            input_type = {"query": "search_query", "document": "search_document"}.get(input_type)

        return [
            EmbeddingType(
                text=string,
                embedding=x,
                cost=self.model.cost_token * self.tokenizer.length_function(string),
                latency=time.perf_counter() - t0,
            )
            for i, x in enumerate(
                self.client.embed(texts=[string], model=self.model.name, input_type=input_type).embeddings
            )
        ]

    @classmethod
    def describe_models(self):
        console.print(cohere_embedding_table)


if __name__ == "__main__":
    CohereEmbedding.describe_models()
    CohereEmbedding.describe_input()
    res = CohereEmbedding(EmbeddingCohereEnglishV3()).embed_str("where is it?", input_type="query")
    logger.info(res)
