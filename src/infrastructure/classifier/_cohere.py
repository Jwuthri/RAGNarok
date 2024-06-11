import logging

from src import API_KEYS, Table, console
from src.infrastructure.tokenizer.base import TokenizerManager
from src.schemas.models import EmbeddingCohereEnglishV2, EmbeddingModel, cohere_table
from src.infrastructure.classifier.base import ClassifierType, ClassifierManager, Example, Label

logger = logging.getLogger(__name__)


class CohereClassifier(ClassifierManager):
    def __init__(self, model: EmbeddingModel) -> None:
        self.model = model
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def classify(self, labels: list[Label], inputs: list[str], examples: list[Example]) -> list[ClassifierType]:
        from cohere import ClassifyExample

        samples = [ClassifyExample(text=example.text, label=example.label.name) for example in examples]
        predictions = self.client.classify(model=self.model.name, inputs=inputs, examples=samples).classifications

        return [
            ClassifierType(
                label=prediction.prediction,
                text=inputs[i],
                cost=self.model.cost_token * TokenizerManager().length_function(inputs[i]),
            )
            for i, prediction in enumerate(predictions)
        ]

    @classmethod
    def describe_models(self):
        console.print(cohere_table)


if __name__ == "__main__":
    CohereClassifier.describe_models()
    # labels = [
    #     Label(name="shipping", description="All messages related to shipping status"),
    #     Label(name="refund", description="All messages related to refund"),
    #     Label(name="other", description="All other categories"),
    # ]
    # examples = [
    #     Example(text="Where is my order?", label=labels[0]),
    #     Example(text="How can I get a refund?", label=labels[1]),
    #     Example(text="What is the weather today", label=labels[2]),
    #     Example(text="track my order?", label=labels[0]),
    #     Example(text="can i get my money back?", label=labels[1]),
    #     Example(text="What is the usa president", label=labels[2]),
    # ]
    # res = CohereClassifier(EmbeddingCohereEnglishV2()).classify(
    #     labels=labels, inputs=["what time is it", "where is my refund?"], examples=examples
    # )
    # logger.info(res)
