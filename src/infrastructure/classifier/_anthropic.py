import logging
from typing import Optional

from src import Table, console
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatModel, ChatAnthropicClaude12
from src.prompts.multi_class_classifier import SYSTEM_MSG, USER_MSG
from src.infrastructure.classifier.base import ClassifierType, ClassifierManager, Example, Label

logger = logging.getLogger(__name__)


class AnthropicClassifier(ClassifierManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import AnthropicChat

            self.client = AnthropicChat(model=model, sync=sync)
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
        table.add_column("DESCRIPTION", justify="left")
        table.add_column("STRENGTHS", justify="left")
        table.add_column("MULTILINGUAL", justify="center")
        table.add_column("VISION", justify="center")
        table.add_column("LATEST API MODEL NAME", justify="left")
        table.add_column("API FORMAT", justify="left")
        table.add_column("COMPARATIVE LATENCY", justify="left")
        table.add_column("CONTEXT WINDOW", justify="left")
        table.add_column("MAX OUTPUT", justify="right")
        table.add_column("COST (Input / Output per MTok)", justify="left")
        table.add_column("TRAINING DATA CUT-OFF", justify="left")

        # Adding rows with the Claude model data
        table.add_row(
            "Claude 3 Opus",
            "Most powerful model for highly complex tasks",
            "Top-level performance, intelligence, fluency, and understanding",
            "Yes",
            "Yes",
            "claude-3-opus-20240229",
            "Messages API",
            "Moderately fast",
            "200K*",
            "4096 tokens",
            "$15.00 / $75.00",
            "Aug 2023",
        )
        table.add_row(
            "Claude 3 Sonnet",
            "Ideal balance of intelligence and speed for enterprise workloads",
            "Maximum utility at a lower price, dependable, balanced for scaled deployments",
            "Yes",
            "Yes",
            "claude-3-sonnet-20240229",
            "Messages API",
            "Fast",
            "200K*",
            "4096 tokens",
            "$3.00 / $15.00",
            "Aug 2023",
        )
        table.add_row(
            "Claude 3 Haiku",
            "Fastest and most compact model for near-instant responsiveness",
            "Quick and accurate targeted performance",
            "Yes",
            "Yes",
            "claude-3-haiku-20240307",
            "Messages API",
            "Fastest",
            "200K*",
            "4096 tokens",
            "$0.25 / $1.25",
            "Aug 2023",
        )
        table.add_row(
            "Claude 2.1",
            "Updated version of Claude 2 with improved accuracy",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-2.1",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "200K*",
            "4096 tokens",
            "$8.00 / $24.0",
            "Early 2023",
        )
        table.add_row(
            "Claude 2",
            "Predecessor to Claude 3, offering strong all-round performance",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-2.0",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "100K**",
            "4096 tokens",
            "$8.00 / $24.0",
            "Early 2023",
        )
        table.add_row(
            "Claude Instant 1.2",
            "Our cheapest small and fast model, a predecessor of Claude Haiku.",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-instant-1.2",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "100K**",
            "4096 tokens",
            "$0.80 / $2.40",
            "Early 2023",
        )

        console.print(table)


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
