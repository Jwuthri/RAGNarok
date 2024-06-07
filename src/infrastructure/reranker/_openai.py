import logging
from typing import Optional

from src import Table, console
from src.infrastructure.reranker.base import RerankType, RerankerManager
from src.prompts.reranker import SYSTEM_MSG, USER_MSG, EXAMPLE, QUERY, DOCS
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt4o

logger = logging.getLogger(__name__)


class OpenaiReranker(RerankerManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import OpenaiChat

            self.client = OpenaiChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

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
    OpenaiReranker.describe_models()
    res = OpenaiReranker(ChatOpenaiGpt4o()).rerank(query=QUERY, documents=DOCS, top_n=5)
    logger.info(res)
