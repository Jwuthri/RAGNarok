import logging

from src.infrastructure.classifier.base import Classifier_typing, ClassifierManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class CohereClassifier(ClassifierManager):
    def __init__(self, model_name: str = "embed-english-v3.0") -> None:
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client("{apiKey}")
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install cohere`")

    def classify(self, examples: list[tuple[str, str]], inputs: list[str]) -> Classifier_typing:
        from cohere import ClassifyExample

        samples = [ClassifyExample(text=example[0], label=example[1]) for example in examples]

        return self.client.classify(model=self.model_name, inputs=inputs, examples=samples).classifications

    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | LATEST MODEL                    | DESCRIPTION                                                                                          | DIMENSIONS | MAX TOKENS (CONTEXT LENGTH) | SIMILARITY METRIC      | ENDPOINTS        |
            |---------------------------------|------------------------------------------------------------------------------------------------------|------------|-----------------------------|------------------------|------------------|
            | embed-multilingual-v3.0         | Provides multilingual classification and embedding support. See supported languages here.            | 1024       | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-multilingual-light-v3.0   | A smaller, faster version of embed-multilingual-v3.0. Almost as capable, but a lot faster.           | 384        | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-multilingual-v2.0         | Provides multilingual classification and embedding support. See supported languages here.            | 768        | 256                         | Dot Product Similarity | Classify, Embed  |
            | embed-english-v3.0              | A model that allows for text to be classified or turned into embeddings. English only.               | 1024       | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-english-light-v3.0        | A smaller, faster version of embed-english-v3.0. Almost as capable, but a lot faster. English only.  | 384        | 512                         | Cosine Similarity      | Embed, Embed Jobs|
            | embed-english-v2.0              | Our older embeddings model that allows for text to be classified or turned into embeddings. English  | 4096       | 512                         | Cosine Similarity      | Classify, Embed  |
            | embed-english-light-v2.0        | A smaller, faster version of embed-english-v2.0. Almost as capable, but a lot faster. English only.  | 1024       | 512                         | Cosine Similarity      | Classify, Embed  |
            """
            )
        )


if __name__ == "__main__":
    x = CohereClassifier()
    x.describe_models()
