import logging

from src.infrastructure.cross_encoder.base import CrossEncoderType, TextCrossEncoderManager, Texts
from src.schemas.models import EmbeddingModel, MSMarcoMiniLML6v2
from src.infrastructure.tokenizer.base import TokenizerManager
from src import Table, console

logger = logging.getLogger(__name__)


class SentenceTransformersCrossEncoder(TextCrossEncoderManager):
    def __init__(self, model: EmbeddingModel):
        self.model = model
        try:
            from sentence_transformers import CrossEncoder
            from torch import nn

            self.client = CrossEncoder(model.name, max_length=512, default_activation_function=nn.Sigmoid())
            self.info_model = {"dimension": model.dimension, "max_seq_length": model.context_size}
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install sentence-transformers`")

    def encode(self, inputs: list[Texts]) -> CrossEncoderType:
        res = self.client.predict([x.texts for x in inputs]).tolist()

        return [
            CrossEncoderType(
                cost=self.model.cost_token * TokenizerManager().length_function(str(inputs[i].texts)),
                texts=inputs[i],
                score=res[i],
            )
            for i in range(len(res))
        ]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model Name", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Dimensions", justify="center")
        table.add_column("Language", justify="left")
        table.add_column("Use Cases", justify="left")
        table.add_column("Accuracy", justify="left")

        # Adding rows with the cross-encoder model data
        table.add_row(
            "ms-marco-TinyBERT-L-2-v2",
            "Cross-encoder model for MS Marco with TinyBERT L-2 architecture",
            "-",
            "English",
            "Information Retrieval",
            "MRR@10: 32.56",
        )
        table.add_row(
            "ms-marco-MiniLM-L-2-v2",
            "Cross-encoder model for MS Marco with MiniLM L-2 architecture",
            "-",
            "English",
            "Information Retrieval",
            "MRR@10: 34.85",
        )
        table.add_row(
            "ms-marco-MiniLM-L-4-v2",
            "Cross-encoder model for MS Marco with MiniLM L-4 architecture",
            "-",
            "English",
            "Information Retrieval",
            "MRR@10: 37.70",
        )
        table.add_row(
            "ms-marco-MiniLM-L-6-v2",
            "Cross-encoder model for MS Marco with MiniLM L-6 architecture",
            "-",
            "English",
            "Information Retrieval",
            "MRR@10: 39.01",
        )
        table.add_row(
            "ms-marco-MiniLM-L-12-v2",
            "Cross-encoder model for MS Marco with MiniLM L-12 architecture",
            "-",
            "English",
            "Information Retrieval",
            "MRR@10: 39.02",
        )
        table.add_row(
            "stsb-TinyBERT-L-4",
            "Cross-encoder model for Semantic Textual Similarity Benchmark with TinyBERT",
            "-",
            "English",
            "Semantic Textual Similarity",
            "STSbenchmark: 85.50",
        )
        table.add_row(
            "stsb-distilroberta-base",
            "Cross-encoder model for Semantic Textual Similarity Benchmark with DistilRoBERTa",
            "-",
            "English",
            "Semantic Textual Similarity",
            "STSbenchmark: 87.92",
        )
        table.add_row(
            "stsb-roberta-base",
            "Cross-encoder model for Semantic Textual Similarity Benchmark with RoBERTa",
            "-",
            "English",
            "Semantic Textual Similarity",
            "STSbenchmark: 90.17",
        )
        table.add_row(
            "stsb-roberta-large",
            "Cross-encoder model for Semantic Textual Similarity Benchmark with large RoBERTa",
            "-",
            "English",
            "Semantic Textual Similarity",
            "STSbenchmark: 91.47",
        )
        table.add_row(
            "quora-distilroberta-base",
            "Cross-encoder model for Quora Question Pairs with DistilRoBERTa",
            "-",
            "English",
            "Duplicate Question Detection",
            "Average Precision: 87.48",
        )
        table.add_row(
            "quora-roberta-base",
            "Cross-encoder model for Quora Question Pairs with RoBERTa",
            "-",
            "English",
            "Duplicate Question Detection",
            "Average Precision: 87.80",
        )
        table.add_row(
            "quora-roberta-large",
            "Cross-encoder model for Quora Question Pairs with large RoBERTa",
            "-",
            "English",
            "Duplicate Question Detection",
            "Average Precision: 87.91",
        )
        table.add_row(
            "nli-deberta-v3-base",
            "Cross-encoder model for Natural Language Inference with DeBERTa v3 base",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 90.04 (MNLI mismatched)",
        )
        table.add_row(
            "nli-deberta-base",
            "Cross-encoder model for Natural Language Inference with DeBERTa base",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 88.08 (MNLI mismatched)",
        )
        table.add_row(
            "nli-deberta-v3-xsmall",
            "Cross-encoder model for Natural Language Inference with DeBERTa v3 xsmall",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 87.77 (MNLI mismatched)",
        )
        table.add_row(
            "nli-deberta-v3-small",
            "Cross-encoder model for Natural Language Inference with DeBERTa v3 small",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 87.55 (MNLI mismatched)",
        )
        table.add_row(
            "nli-roberta-base",
            "Cross-encoder model for Natural Language Inference with RoBERTa base",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 87.47 (MNLI mismatched)",
        )
        table.add_row(
            "nli-MiniLM2-L6-H768",
            "Cross-encoder model for Natural Language Inference with MiniLM2 L6 H768",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 86.89 (MNLI mismatched)",
        )
        table.add_row(
            "nli-distilroberta-base",
            "Cross-encoder model for Natural Language Inference with DistilRoBERTa base",
            "-",
            "English",
            "Natural Language Inference",
            "Accuracy: 83.98 (MNLI mismatched)",
        )

        console.print(table)


if __name__ == "__main__":
    SentenceTransformersCrossEncoder.describe_models()
    texts = [Texts(texts=("where is it?", "why is it?")), Texts(texts=("what is it?", "who is it?"))]
    res = SentenceTransformersCrossEncoder(MSMarcoMiniLML6v2()).encode(texts)
    logger.info(res)
