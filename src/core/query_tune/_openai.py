import logging
from typing import Optional

from src import console
from src.core.query_tune.base import QueryTuneManager, QueryTuneType
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt4o, openai_table
from src.prompts.query_tune import *
from src.core.completion_parser import ListParser, StringParser

logger = logging.getLogger(__name__)


class OpenaiQueryRefiner(QueryTuneManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True, to_db: bool = False) -> None:
        self.to_db = to_db
        try:
            from src.core.chat import OpenaiChat

            self.client = OpenaiChat(model=model, sync=sync)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install openai`")

    def expand(self, query: str, n: Optional[int] = 3) -> QueryTuneType:
        messages = [
            ChatMessageSchema(
                role="system",
                message=SYSTEM_MSG_EXPAND.replace("$NUMBER_QUERIES", str(n)).replace("$EXAMPLES", EXAMPLE_EXPAND),
            ),
            ChatMessageSchema(role="user", message=USER_MSG.replace("$INPUT", query)),
        ]
        prediction = self.client.predict(messages=messages)
        prediction_parsed = ListParser.parse(text=prediction.prediction)
        messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return QueryTuneType(
            original_query=query,
            expanded_queries=prediction_parsed.parsed_completion,
            func="expand",
            cost=prediction.cost,
            latency=prediction.latency,
        )

    def refine(self, query: str) -> QueryTuneType:
        messages = [
            ChatMessageSchema(role="system", message=SYSTEM_MSG_REFINE.replace("$EXAMPLES", EXAMPLE_REFINE)),
            ChatMessageSchema(role="user", message=USER_MSG.replace("$INPUT", query)),
        ]
        prediction = self.client.predict(messages=messages)
        prediction_parsed = StringParser.parse(text=prediction.prediction)
        messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return QueryTuneType(
            original_query=query,
            refined_query=prediction_parsed.parsed_completion,
            func="refine",
            cost=prediction.cost,
            latency=prediction.latency,
        )

    def divide(self, query: str) -> QueryTuneType:
        messages = [
            ChatMessageSchema(role="system", message=SYSTEM_MSG_DIVIDE.replace("$EXAMPLES", EXAMPLE_DIVIDE)),
            ChatMessageSchema(role="user", message=USER_MSG.replace("$INPUT", query)),
        ]
        prediction = self.client.predict(messages=messages)
        prediction_parsed = ListParser.parse(text=prediction.prediction)
        messages.append(ChatMessageSchema(role="assistant", message=prediction.prediction))

        return QueryTuneType(
            original_query=query,
            divided_queries=prediction_parsed.parsed_completion,
            func="divide",
            cost=prediction.cost,
            latency=prediction.latency,
        )

    @classmethod
    def describe_models(self):
        console.print(openai_table)


if __name__ == "__main__":
    OpenaiQueryRefiner.describe_models()
    res = OpenaiQueryRefiner(ChatOpenaiGpt4o()).expand(
        query="I was wondering if I can extract data from my blog into my knowledge data llm?"
    )
    logger.info(res)
    res = OpenaiQueryRefiner(ChatOpenaiGpt4o()).refine(
        query="I was wondering if I can extract data from my blog into my knowledge data llm?"
    )
    logger.info(res)
    res = OpenaiQueryRefiner(ChatOpenaiGpt4o()).divide(
        query="I was wondering if I can extract data from my blog into my knowledge data llm?"
    )
    logger.info(res)
