import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, EmbeddingManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class SentenceTransformersEmbedding(EmbeddingManager):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer

            self.embeddings = SentenceTransformer(model_name)
            self.info_model = {
                "dimension": self.embeddings.get_sentence_embedding_dimension(),
                "max_seq_length": self.embeddings.max_seq_length,
            }
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install sentence-transformers`")

    def embed_batch(self, batch: list[str]) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of each string in the input list.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.embeddings.encode(batch, show_progress_bar=False).tolist()

    def embed_str(self, string: str) -> Embedding_typing:
        """
        This function takes a string query and returns its embedding as a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.embeddings.encode([string], show_progress_bar=False).tolist()[0]

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | Model Name                                | Description                                                                    | Dimensions | Language     | Use Cases                           |
            |-------------------------------------------|--------------------------------------------------------------------------------|------------|--------------|-------------------------------------|
            | roberta-base-nli-mean-tokens              | RoBERTa-based model trained for sentence embeddings with mean pooling          | 768        | English      | General purpose sentence embedding  |
            | distilroberta-base-nli-mean-tokens        | DistilRoBERTa-based model trained for sentence embeddings with mean pooling    | 768        | English      | General purpose sentence embedding  |
            | paraphrase-xlm-r-multilingual-v1          | Multilingual model trained for paraphrase identification task                  | 768        | Multilingual | Paraphrase identification           |
            | stsb-xlm-r-multilingual                   | Multilingual model trained for Semantic Textual Similarity Benchmark (STSB)    | 768        | Multilingual | Semantic Textual Similarity         |
            | msmarco-distilroberta-base-v4             | DistilRoBERTa-based model trained for MS Marco dataset                         | 768        | English      | Information Retrieval               |
            | msmarco-roberta-base-v2                   | RoBERTa-based model trained for MS Marco dataset                               | 768        | English      | Information Retrieval               |
            | distiluse-base-multilingual-cased-v1      | Multilingual model trained for sentence embeddings with mean pooling           | 512        | Multilingual | General purpose sentence embedding  |
            | average_word_embeddings_glove.6B.300d     | GloVe-based model with average pooling for word embeddings                     | 300        | English      | Word embeddings                     |
            | average_word_embeddings_glove.840B.300d   | GloVe-based model with average pooling for word embeddings                     | 300        | English      | Word embeddings                     |
            | average_word_embeddings_glove.42B.300d    | GloVe-based model with average pooling for word embeddings                     | 300        | English      | Word embeddings                     |
            | average_word_embeddings_fasttext.en.300d  | FastText-based model with average pooling for word embeddings                  | 300        | English      | Word embeddings                     |
            | average_word_embeddings_fasttext.42B.300d | FastText-based model with average pooling for word embeddings                  | 300        | English      | Word embeddings                     |
            | average_word_embeddings_fasttext.300d     | FastText-based model with average pooling for word embeddings                  | 300        | English      | Word embeddings                     |
            | multi-qa-MiniLM-L6-cos-v1                 | Model designed for QA tasks, leveraging MiniLM architecture for cos similarity | 384        | Multiple     | QA, Semantic Search                 |
            | msmarco-MiniLM-L6-cos-v5                  | Optimized for MSMARCO passage ranking, producing normalized vectors            | 384        | English      | Passage ranking, Semantic Search    |
            | clip-ViT-B-32-multilingual-v1             | Embeds both images and text, extending clip-ViT-B-32 to 50+ languages          | 512        | 50 Languages | Text2Image search, Image clustering |
            | hkunlp/instructor-large                   | Instructor models trained with instructions in mind for dynamic tasks          | 768        | English      | Information retrieval, Clustering   |
            | all-MiniLM-L6-v2                          | MiniLM architecture for cos similarity                                         | 384        | English      | QA, Semantic Search                 |
            """
            )
        )


if __name__ == "__main__":
    SentenceTransformersEmbedding.describe_models()
