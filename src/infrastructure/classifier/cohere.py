import logging

from src.infrastructure.classifier.base import Classifier_typing, ClassifierManager

logger = logging.getLogger(__name__)


class CohereClassifier(ClassifierManager):
    def __init__(self, model_name: str = "embed-english-v2.0") -> None:
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client("{apiKey}")
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def classify(self, examples: list[tuple[str, str]], inputs: list[str]) -> Classifier_typing:
        from cohere import ClassifyExample

        samples = [ClassifyExample(text=example[0], label=example[1]) for example in examples]

        return self.client.classify(model=self.model_name, inputs=inputs, examples=samples).classifications
