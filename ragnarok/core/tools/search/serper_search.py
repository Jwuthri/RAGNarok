from typing import Optional
import logging
import json
import requests

from ragnarok import API_KEYS
from ragnarok.core.tools import run_tool
from ragnarok.core.tools.tools_generator import FunctionToOpenAITool
from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.models import ChatOpenaiGpt35
from ragnarok.core.chat import OpenaiChat

logger = logging.getLogger(__name__)


class SerperSearchTool:
    def __init__(self, api_key: str = API_KEYS.GOOGLE_SERPER_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        self.base_url = "https://google.serper.dev/{query_type}"
        self.search_kwargs = search_kwargs

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
        payload = json.dumps({"q": query})
        response = requests.request(
            "POST", self.base_url.format(query_type=query_type), headers=self.headers, data=payload
        )

        return response.json()


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
    columns = {"news": ["news"], "search": ["organic", "peopleAlsoAsk"]}
    answer = []
    logger.info(search_res)
    for column in columns.get(query_type, search_res.keys()):
        for res in search_res.get(column):
            answer.append(
                {
                    "title": res.get("title"),
                    "description": res.get("snippet"),
                    "question": res.get("question"),
                    "url": res.get("link"),
                    "date": res.get("date"),
                }
            )

    return answer


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(search_tool).generate_tool_json()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="how many employees at Gainsight in 2024? and where are they located"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    logger.info(res)
    func_res = []
    if res.tools_call:
        for tool in res.tools_call:
            _func_res = run_tool(tool, {"search_tool": search_tool})

    func_res.append(_func_res)
    logger.info(func_res)
    breakpoint()
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
