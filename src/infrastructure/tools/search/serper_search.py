import logging
from typing import Optional

import http.client
import json

from src import API_KEYS
from src.infrastructure.tools import run_tool
from src.infrastructure.tools.tools_generator import FunctionToOpenAITool
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatOpenaiGpt35
from src.infrastructure.chat import OpenaiChat

logger = logging.getLogger(__name__)


class SerperSearchTool:
    def __init__(self, api_key: str = API_KEYS.GOOGLE_SERPER_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    def search(self, query: str, query_type: str = "search") -> list[dict]:
        """
        The function performs a search query using the specified query type and returns the decoded
        response data.

        :param query: The `query` parameter is a string that represents the search query that you want
        to perform on the specified search engine
        :type query: str
        :param query_type: The `query_type` parameter in the `search` method specifies the type of
        search to be performed. It has a default value of "search" but can also be set to "videos",
        "news", or "images" based on the type of search you want to conduct, defaults to search
        :type query_type: str (optional)
        :return: the decoded data as a string in UTF-8 format.
        """
        assert query_type in ["search", "videos", "news", "images"]

        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        conn.request("POST", f"/{query_type}", payload, self.headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")


def search_tool(query: str, query_type: str) -> list[dict]:
    """
    The function `search_tool` takes a search query and query type as input, performs a search using a
    search tool, and returns the search results as a list of dictionaries.

    :param query: The `query` parameter is a string that represents the search query that the user wants
    to search for. It could be a keyword, phrase, or question that the user wants to find information
    about
    :param query_type: The `query_type` parameter in the `search` method specifies the type of
    search to be performed. It has a default value of "search" but can also be set to "videos",
    "news", or "images" based on the type of search you want to conduct, defaults to search
    :type query_type: str (optional)
    :return: A list of dictionaries containing search results.
    """
    search_res = SerperSearchTool().search(query=query, query_type=query_type)

    return search_res


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(search_tool).generate_tool_json()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="how many employees at Deepgram in 2024?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    logger.info(res)
    func_res = run_tool(res.tool_call, {"search_tool": search_tool})
    logger.info(func_res)
    if func_res:
        messages = [
            ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
            ChatMessageSchema(
                role="user",
                message=f"how many employees at Deepgram, and where are they based?\nhere are some data: {func_res}",
            ),
        ]
        res = OpenaiChat(ChatOpenaiGpt35()).predict(messages)
        logger.info(res)
