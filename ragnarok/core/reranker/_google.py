import logging
from typing import Optional

from ragnarok import console
from ragnarok.core.reranker.base import RerankType, RerankerManager
from ragnarok.prompts.reranker import SYSTEM_MSG, USER_MSG, EXAMPLE, QUERY, DOCS
from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.models import ChatModel, ChatGoogleGeminiPro1, google_table

logger = logging.getLogger(__name__)


class GoogleReranker(RerankerManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        try:
            from ragnarok.core.chat import GoogleChat

            self.client = GoogleChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install google-generativeai`")

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
        console.print(google_table)


if __name__ == "__main__":
    GoogleReranker.describe_models()
    res = GoogleReranker(ChatGoogleGeminiPro1()).rerank(query=QUERY, documents=DOCS, top_n=5)
    logger.info(res)
