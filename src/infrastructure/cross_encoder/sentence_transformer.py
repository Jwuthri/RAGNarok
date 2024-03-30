import logging

from src.infrastructure.cross_encoder.base import CrossEncoder_typing, TextCrossEncoderManager

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
