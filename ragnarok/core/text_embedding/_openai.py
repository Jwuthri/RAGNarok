import logging
import time

from ragnarok.core.text_embedding.base import EmbeddingType, EmbeddingManager, InputType
from ragnarok import console, API_KEYS
from ragnarok.schemas.models import EmbeddingModel, EmbeddingOpenaiSmall3, openai_embedding_table
from ragnarok.core.tokenizer import OpenaiTokenizer

logger = logging.getLogger(__name__)


class OpenaiEmbedding(EmbeddingManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        self.tokenizer = OpenaiTokenizer(model)
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=API_KEYS.OPENAI_API_KEY)
            self.info_model = {"dimension": self.model.dimension, "max_seq_length": self.model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

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
                embedding=x.embedding,
                cost=self.model.cost_token * self.tokenizer.length_function(batch[i]),
                latency=time.perf_counter() - t0,
            )
            for i, x in enumerate(self.client.embeddings.create(input=batch, model=self.model.name).data)
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
                embedding=x.embedding,
                cost=self.model.cost_token * self.tokenizer.length_function(string),
                latency=time.perf_counter() - t0,
            )
            for i, x in enumerate(self.client.embeddings.create(input=[string], model=self.model.name).data)
        ][0]

    @classmethod
    def describe_models(self):
        console.print(openai_embedding_table)


if __name__ == "__main__":
    OpenaiEmbedding.describe_models()
    res = OpenaiEmbedding(EmbeddingOpenaiSmall3()).embed_str("where is it?", input_type="search_query")
    logger.info(res)
