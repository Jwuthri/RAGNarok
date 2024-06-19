import logging
from typing import Optional

from src import console
from src.infrastructure.reranker.base import RerankType, RerankerManager
from src.prompts.reranker import SYSTEM_MSG, USER_MSG, EXAMPLE, QUERY, DOCS
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt4o, openai_table

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
            RerankType(
                query=query,
                new_index=i,
                previous_index=x,
                score=1.0 / (i + 1),
                document=documents[x],
                cost=prediction.cost,
                latency=prediction.latency,
            )
            for i, x in enumerate(parsed_predictions.parsed_completion)
        ][:top_n]

        return predictions

    @classmethod
    def describe_models(self):
        console.print(openai_table)


if __name__ == "__main__":
    OpenaiReranker.describe_models()
    res = OpenaiReranker(ChatOpenaiGpt4o()).rerank(query=QUERY, documents=DOCS, top_n=5)
    logger.info(res)
