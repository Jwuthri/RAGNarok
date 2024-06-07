import logging
from typing import Optional

from src import Table, console
from src.infrastructure.reranker.base import RerankType, RerankerManager
from src.prompts.reranker import SYSTEM_MSG, USER_MSG, EXAMPLE, QUERY, DOCS
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatGoogleGeminiPro1

logger = logging.getLogger(__name__)


class GoogleClassifier(RerankerManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from src.infrastructure.chat import GoogleChat

            self.client = GoogleChat(model=model, sync=sync)
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
        table.add_column("RATE LIMITS", justify="left")
        table.add_column("PRICING (INPUT/OUTPUT)", justify="left")

        table.add_row("Gemini-Pro 1.0", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50 per 1 million tokens")
        table.add_row("Gemini-Pro Vision 1.0", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50 per 1 million tokens")
        table.add_row(
            "Gemini-Pro 1.5", "5 RPM, 10 million TPM, 2,000 RPD", "$7 / $21 per 1 million tokens (preview pricing)"
        )

        console.print(table)


if __name__ == "__main__":
    GoogleClassifier.describe_models()
    res = GoogleClassifier(ChatGoogleGeminiPro1()).rerank(query=QUERY, documents=DOCS, top_n=5)
    logger.info(res)
