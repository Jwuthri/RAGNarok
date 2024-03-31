import logging

from src.infrastructure.cross_encoder.base import CrossEncoder_typing, TextCrossEncoderManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class SentenceTransformersCrossEncoder(TextCrossEncoderManager):
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        try:
            from sentence_transformers import CrossEncoder
            from torch import nn

            self.model = CrossEncoder(model_name, max_length=512, default_activation_function=nn.Sigmoid())
            self.info_model = {
                "dimension": self.model.config.hidden_size,
                "max_seq_length": self.model.max_length,
            }
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install torch`")
            logger.warning("Please run `pip install sentence-transformers`")

    def encode(self, batch: list[tuple[str, str]]) -> CrossEncoder_typing:
        return self.model.predict(batch).tolist()

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | Model Name               | Description                                                                      | Dimensions | Language | Use Cases                    | Accuracy                          |
            |--------------------------|----------------------------------------------------------------------------------|------------|----------|------------------------------|-----------------------------------|
            | ms-marco-TinyBERT-L-2-v2 | Cross-encoder model for MS Marco with TinyBERT L-2 architecture                  | -          | English  | Information Retrieval        | MRR@10: 32.56                     |
            | ms-marco-MiniLM-L-2-v2   | Cross-encoder model for MS Marco with MiniLM L-2 architecture                    | -          | English  | Information Retrieval        | MRR@10: 34.85                     |
            | ms-marco-MiniLM-L-4-v2   | Cross-encoder model for MS Marco with MiniLM L-4 architecture                    | -          | English  | Information Retrieval        | MRR@10: 37.70                     |
            | ms-marco-MiniLM-L-6-v2   | Cross-encoder model for MS Marco with MiniLM L-6 architecture                    | -          | English  | Information Retrieval        | MRR@10: 39.01                     |
            | ms-marco-MiniLM-L-12-v2  | Cross-encoder model for MS Marco with MiniLM L-12 architecture                   | -          | English  | Information Retrieval        | MRR@10: 39.02                     |
            | stsb-TinyBERT-L-4        | Cross-encoder model for Semantic Textual Similarity Benchmark with TinyBERT      | -          | English  | Semantic Textual Similarity  | STSbenchmark: 85.50               |
            | stsb-distilroberta-base  | Cross-encoder model for Semantic Textual Similarity Benchmark with DistilRoBERTa | -          | English  | Semantic Textual Similarity  | STSbenchmark: 87.92               |
            | stsb-roberta-base        | Cross-encoder model for Semantic Textual Similarity Benchmark with RoBERTa       | -          | English  | Semantic Textual Similarity  | STSbenchmark: 90.17               |
            | stsb-roberta-large       | Cross-encoder model for Semantic Textual Similarity Benchmark with large RoBERTa | -          | English  | Semantic Textual Similarity  | STSbenchmark: 91.47               |
            | quora-distilroberta-base | Cross-encoder model for Quora Question Pairs with DistilRoBERTa                  | -          | English  | Duplicate Question Detection | Average Precision: 87.48          |
            | quora-roberta-base       | Cross-encoder model for Quora Question Pairs with RoBERTa                        | -          | English  | Duplicate Question Detection | Average Precision: 87.80          |
            | quora-roberta-large      | Cross-encoder model for Quora Question Pairs with large RoBERTa                  | -          | English  | Duplicate Question Detection | Average Precision: 87.91          |
            | nli-deberta-v3-base      | Cross-encoder model for Natural Language Inference with DeBERTa v3 base          | -          | English  | Natural Language Inference   | Accuracy: 90.04 (MNLI mismatched) |
            | nli-deberta-base         | Cross-encoder model for Natural Language Inference with DeBERTa base             | -          | English  | Natural Language Inference   | Accuracy: 88.08 (MNLI mismatched) |
            | nli-deberta-v3-xsmall    | Cross-encoder model for Natural Language Inference with DeBERTa v3 xsmall        | -          | English  | Natural Language Inference   | Accuracy: 87.77 (MNLI mismatched) |
            | nli-deberta-v3-small     | Cross-encoder model for Natural Language Inference with DeBERTa v3 small         | -          | English  | Natural Language Inference   | Accuracy: 87.55 (MNLI mismatched) |
            | nli-roberta-base         | Cross-encoder model for Natural Language Inference with RoBERTa base             | -          | English  | Natural Language Inference   | Accuracy: 87.47 (MNLI mismatched) |
            | nli-MiniLM2-L6-H768      | Cross-encoder model for Natural Language Inference with MiniLM2 L6 H768          | -          | English  | Natural Language Inference   | Accuracy: 86.89 (MNLI mismatched) |
            | nli-distilroberta-base   | Cross-encoder model for Natural Language Inference with DistilRoBERTa base       | -          | English  | Natural Language Inference   | Accuracy: 83.98 (MNLI mismatched) |

            """
            )
        )


if __name__ == "__main__":
    SentenceTransformersCrossEncoder.describe_models()
