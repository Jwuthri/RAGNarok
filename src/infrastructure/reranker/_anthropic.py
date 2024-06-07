import logging
from typing import Optional

from src import Table, console
from src.infrastructure.reranker.base import RerankType, RerankerManager
from src.prompts.reranker import SYSTEM_MSG, USER_MSG, EXAMPLE, QUERY, DOCS
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatAnthropicClaude3Sonnet

logger = logging.getLogger(__name__)


class AnthropicClassifier(RerankerManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import AnthropicChat

            self.client = AnthropicChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install anthropic`")

    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankType]:
        docs = "\n".join([f"ID {i}: {doc}" for i, doc in enumerate(documents)])
        messages = [
            ChatMessageSchema(role="system", message=SYSTEM_MSG.replace("$EXAMPLES", EXAMPLE)),
            ChatMessageSchema(role="user", message=USER_MSG.replace("$DOCUMENTS", docs).replace("$QUERY", query)),
        ]
        prediction = self.client.predict(messages=messages)
        parsed_predictions = self.parse_completion(completion=prediction.prediction)
        messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))
        predictions = [
            RerankType(query=query, new_index=i, previous_index=x, score=1.0 / (i + 1), document=documents[x])
            for i, x in enumerate(parsed_predictions.parsed_completion)
        ][:top_n]

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
    res = AnthropicClassifier(ChatAnthropicClaude3Sonnet()).rerank(query=QUERY, documents=DOCS, top_n=5)
    logger.info(res)
