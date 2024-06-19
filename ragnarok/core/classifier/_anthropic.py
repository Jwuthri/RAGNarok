import logging
from typing import Optional

from ragnarok import console
from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.models import ChatModel, ChatAnthropicClaude12, anthropic_table
from ragnarok.prompts.multi_class_classifier import SYSTEM_MSG, USER_MSG
from ragnarok.core.classifier.base import ClassifierType, ClassifierManager, Example, Label

logger = logging.getLogger(__name__)


class AnthropicClassifier(ClassifierManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True, to_db: bool = False) -> None:
        self.to_db = to_db
        try:
            from ragnarok.core.chat import AnthropicChat

            self.client = AnthropicChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install anthropic`")

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
            predictions.append(
                ClassifierType(
                    label=prediction.prediction, text=input, cost=prediction.cost, latency=prediction.latency
                )
            )
            messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return predictions

    @classmethod
    def describe_models(self):
        console.print(anthropic_table)


if __name__ == "__main__":
    AnthropicClassifier.describe_models()
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
    res = AnthropicClassifier(ChatAnthropicClaude12()).classify(
        labels=labels, inputs=["where is my refund?", "how can i track my order"], examples=examples
    )
    logger.info(res)
