import logging
from typing import Optional

from src import Table, console
from src.infrastructure.classifier.base import ClassifierType, ClassifierManager, Example, Label
from src.prompts.multi_class_classifier import SYSTEM_MSG, USER_MSG
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt35, openai_table

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
        messages = [
            ChatMessageSchema(
                role="system", message=SYSTEM_MSG.replace("$CLASSES", str(classes)).replace("$EXAMPLES", samples)
            )
        ]
        predictions = []
        for input in inputs:
            messages.append(ChatMessageSchema(role="user", message=USER_MSG.replace("$INPUT", input)))
            prediction = self.client.predict(messages=messages)
            predictions.append(ClassifierType(label=prediction.prediction, text=input, cost=prediction.cost))
            messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return predictions

    @classmethod
    def describe_models(self):
        console.print(openai_table)


if __name__ == "__main__":
    OpenaiClassifier.describe_models()
    # labels = [
    #     Label(name="shipping", description="All messages related to shipping status"),
    #     Label(name="refund", description="All messages related to refund"),
    #     Label(name="other", description="All other categories"),
    # ]
    # examples = [
    #     Example(text="Where is my order?", label=labels[0]),
    #     Example(text="How can I get a refund?", label=labels[1]),
    #     Example(text="What is the weather today", label=labels[2]),
    # ]
    # res = OpenaiClassifier(ChatOpenaiGpt35()).classify(
    #     labels=labels, inputs=["where is my refund?", "how can i track my order"], examples=examples
    # )
    # logger.info(res)
