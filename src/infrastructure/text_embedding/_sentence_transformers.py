import logging
from typing import Literal

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, EmbeddingManager
from src import Table, CONSOLE
from src.schemas.models import EmbeddingModel

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

    def embed_batch(
        self, batch: list[str], input_type: Literal["system", "user", "assistant"] = None
    ) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of each string in the input list.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.client.encode(batch, show_progress_bar=False).tolist()

    def embed_str(self, string: str, input_type: Literal["system", "user", "assistant"] = None) -> Embedding_typing:
        """
        This function takes a string query and returns its embedding as a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.client.encode([string], show_progress_bar=False).tolist()[0]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model Name", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Dimensions", justify="left")
        table.add_column("Language", justify="left")
        table.add_column("Use Cases", justify="left")

        table.add_row(
            "roberta-base-nli-mean-tokens",
            "RoBERTa-based model trained for sentence embeddings with mean pooling",
            "768",
            "English",
            "General purpose sentence embedding",
        )
        table.add_row(
            "distilroberta-base-nli-mean-tokens",
            "DistilRoBERTa-based model trained for sentence embeddings with mean pooling",
            "768",
            "English",
            "General purpose sentence embedding",
        )
        table.add_row(
            "paraphrase-xlm-r-multilingual-v1",
            "Multilingual model trained for paraphrase identification task",
            "768",
            "Multilingual",
            "Paraphrase identification",
        )
        table.add_row(
            "stsb-xlm-r-multilingual",
            "Multilingual model trained for Semantic Textual Similarity Benchmark (STSB)",
            "768",
            "Multilingual",
            "Semantic Textual Similarity",
        )
        table.add_row(
            "msmarco-distilroberta-base-v4",
            "DistilRoBERTa-based model trained for MS Marco dataset",
            "768",
            "English",
            "Information Retrieval",
        )
        table.add_row(
            "msmarco-roberta-base-v2",
            "RoBERTa-based model trained for MS Marco dataset",
            "768",
            "English",
            "Information Retrieval",
        )
        table.add_row(
            "distiluse-base-multilingual-cased-v1",
            "Multilingual model trained for sentence embeddings with mean pooling",
            "512",
            "Multilingual",
            "General purpose sentence embedding",
        )
        table.add_row(
            "multi-qa-MiniLM-L6-cos-v1",
            "Model designed for QA tasks, leveraging MiniLM architecture for cos similarity",
            "384",
            "Multiple",
            "QA, Semantic Search",
        )
        table.add_row(
            "msmarco-MiniLM-L6-cos-v5",
            "Optimized for MSMARCO passage ranking, producing normalized vectors",
            "384",
            "English",
            "Passage ranking, Semantic Search",
        )
        table.add_row(
            "clip-ViT-B-32-multilingual-v1",
            "Embeds both images and text, extending clip-ViT-B-32 to 50+ languages",
            "512",
            "50 Languages",
            "Text2Image search, Image clustering",
        )
        table.add_row(
            "hkunlp/instructor-large",
            "Instructor models trained with instructions in mind for dynamic tasks",
            "768",
            "English",
            "Information retrieval, Clustering",
        )
        table.add_row(
            "all-MiniLM-L6-v2", "MiniLM architecture for cos similarity", "384", "English", "QA, Semantic Search"
        )

        CONSOLE.print(table)


if __name__ == "__main__":
    SentenceTransformersEmbedding.describe_models()
    SentenceTransformersEmbedding.describe_input()
    model = EmbeddingModel(context_size=512, cost_token=0, dimension=384, metric="cosine", name="all-MiniLM-L6-v2")
    res = SentenceTransformersEmbedding(model).embed_str("where is it?", input_type="search_query")
    logger.info(res)
