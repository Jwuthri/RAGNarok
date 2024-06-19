import logging
import time

from ragnarok.core.cross_encoder.base import CrossEncoderType, TextCrossEncoderManager, Texts
from ragnarok.schemas.models import EmbeddingModel, MSMarcoMiniLML6v2, hf_crossencoder_table
from ragnarok.core.tokenizer.base import TokenizerManager
from ragnarok import console

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
        t0 = time.perf_counter()
        res = self.client.predict([x.texts for x in inputs]).tolist()

        return [
            CrossEncoderType(
                cost=self.model.cost_token * TokenizerManager().length_function(str(inputs[i].texts)),
                texts=inputs[i],
                score=res[i],
                latency=time.perf_counter() - t0,
            )
            for i in range(len(res))
        ]

    @classmethod
    def describe_models(self):
        console.print(hf_crossencoder_table)


if __name__ == "__main__":
    SentenceTransformersCrossEncoder.describe_models()
    texts = [Texts(texts=("where is it?", "why is it?")), Texts(texts=("what is it?", "who is it?"))]
    res = SentenceTransformersCrossEncoder(MSMarcoMiniLML6v2()).encode(texts)
    logger.info(res)
