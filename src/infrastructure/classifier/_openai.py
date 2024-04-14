import logging
from typing import Optional

from src import Table, console
from src.infrastructure.classifier.base import ClassifierType, ClassifierManager, Example, Label
from src.prompts.multi_class_classifier import SYSTEM_MSG, USER_MSG
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt35

logger = logging.getLogger(__name__)


class OpenaiClassifier(ClassifierManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import OpenaiChat

            self.client = OpenaiChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

    def classify(self, labels: list[Label], inputs: list[str], examples: list[Example]) -> list[ClassifierType]:
        classes = {label.name: label.description for label in labels}
        samples = "\n---".join([f"## Input: {example.text}\n## Output: {example.label.name}" for example in examples])
        messages = [ChatMessageSchema(role="system", message=SYSTEM_MSG.format(CLASSES=classes, EXAMPLES=samples))]
        predictions = []
        for input in inputs:
            messages.append(ChatMessageSchema(role="user", message=USER_MSG.format(INPUT=input)))
            prediction = self.client.predict(messages=messages)
            predictions.append(ClassifierType(label=prediction.prediction, text=input, cost=prediction.cost))
            messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return predictions

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("MODEL", justify="left")
        table.add_column("DESCRIPTION", justify="left")
        table.add_column("CONTEXT LENGTH", justify="right")
        table.add_row(
            "gpt-4-0125-preview", "New GPT-4 Turbo intended to reduce 'laziness'.", "128,000 tokens / Up to Dec 2023"
        )
        table.add_row("gpt-4-turbo-preview", "Points to gpt-4-0125-preview.", "128,000 tokens / Up to Dec 2023")
        table.add_row(
            "gpt-4-1106-preview",
            "Features improved instruction following, JSON mode, and more.",
            "128,000 tokens / Up to Apr 2023",
        )
        table.add_row(
            "gpt-4-vision-preview", "GPT-4 with image understanding capabilities.", "128,000 tokens / Up to Apr 2023"
        )
        table.add_row("gpt-4", "Currently points to gpt-4-0613.", "8,192 tokens / Up to Sep 2021")
        table.add_row(
            "gpt-3.5-turbo-0125", "Latest GPT-3.5 Turbo model with higher accuracy.", "16,385 tokens / Up to Sep 2021"
        )
        table.add_row("gpt-3.5-turbo", "Points to gpt-3.5-turbo-0125.", "16,385 tokens / Up to Sep 2021")
        table.add_row(
            "gpt-3.5-turbo-instruct",
            "Similar capabilities as GPT-3 models, for legacy endpoints.",
            "4,096 tokens / Up to Sep 2021",
        )
        console.print(table)


if __name__ == "__main__":
    OpenaiClassifier.describe_models()
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
    res = OpenaiClassifier(ChatOpenaiGpt35()).classify(
        labels=labels, inputs=["where is my refund?", "how can i track my order"], examples=examples
    )
    logger.info(res)
