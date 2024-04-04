import logging
from typing import Optional

from src import Table, CONSOLE
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatModel, ChatGoogleGeminiPro1
from src.prompts.multi_class_classifier import SYSTEM_MSG, USER_MSG
from src.infrastructure.classifier.base import ClassifierType, ClassifierManager, Example, Label

logger = logging.getLogger(__name__)


class GoogleClassifier(ClassifierManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import GoogleChat

            self.client = GoogleChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install anthropic`")

    def classify(self, labels: list[Label], inputs: list[str], examples: list[Example]) -> list[ClassifierType]:
        classes = {label.name: label.description for label in labels}
        samples = "\n---".join([f"## Input: {example.text}\n## Output: {example.label.name}" for example in examples])
        messages = [ChatMessage(role="system", message=SYSTEM_MSG.format(CLASSES=classes, EXAMPLES=samples))]
        predictions = []
        for input in inputs:
            messages.append(ChatMessage(role="user", message=USER_MSG.format(INPUT=input)))
            prediction = self.client.predict(messages=messages)
            predictions.append(ClassifierType(label=prediction.prediction, text=input, cost=prediction.cost))
            messages.append(ChatMessage(role="assistant", message=prediction.prediction))

        return predictions

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("MODEL", justify="left")
        table.add_column("RATE LIMITS", justify="left")
        table.add_column("PRICING (INPUT/OUTPUT)", justify="left")

        table.add_row("Gemini-Pro 1.0", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50 per 1 million tokens")
        table.add_row("Gemini-Pro Vision 1.0", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50 per 1 million tokens")
        table.add_row(
            "Gemini-Pro 1.5", "5 RPM, 10 million TPM, 2,000 RPD", "$7 / $21 per 1 million tokens (preview pricing)"
        )

        CONSOLE.print(table)


if __name__ == "__main__":
    GoogleClassifier.describe_models()
    labels = [
        Label(name="shipping", description="All messages related to shipping status"),
        Label(name="refund", description="All messages related to refund"),
        Label(name="other", description="All other categories"),
    ]
    examples = [
        Example(text="Where is my order?", label=labels[0]),
        Example(text="How can I get a refund?", label=labels[1]),
        Example(text="What is the weather today", label=labels[2]),
    ]
    res = GoogleClassifier(ChatGoogleGeminiPro1()).classify(
        labels=labels, inputs=["where is my refund?", "how can i track my order"], examples=examples
    )
    logger.info(res)
