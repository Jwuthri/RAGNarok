import logging

from src import API_KEYS
from src.infrastructure.classifier.base import Classifier_typing, ClassifierManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class CohereClassifier(ClassifierManager):
    def __init__(self, model_name: str = "embed-english-v2.0") -> None:
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def classify(self, examples: list[tuple[str, str]], inputs: list[str]) -> Classifier_typing:
        from cohere import ClassifyExample

        samples = [ClassifyExample(text=example[0], label=example[1]) for example in examples]

        return self.client.classify(model=self.model_name, inputs=inputs, examples=samples).classifications

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | LATEST MODEL                    | DESCRIPTION                                                                                          | DIMENSIONS | MAX TOKENS (CONTEXT LENGTH) | SIMILARITY METRIC      | ENDPOINTS        |
            |---------------------------------|------------------------------------------------------------------------------------------------------|------------|-----------------------------|------------------------|------------------|
            | embed-multilingual-v2.0         | Provides multilingual classification and embedding support. See supported languages here.            | 768        | 256                         | Dot Product Similarity | Classify, Embed  |
            | embed-english-v2.0              | Our older embeddings model that allows for text to be classified or turned into embeddings. English  | 4096       | 512                         | Cosine Similarity      | Classify, Embed  |
            | embed-english-light-v2.0        | A smaller, faster version of embed-english-v2.0. Almost as capable, but a lot faster. English only.  | 1024       | 512                         | Cosine Similarity      | Classify, Embed  |
            """
            )
        )


if __name__ == "__main__":
    CohereClassifier.describe_models()
