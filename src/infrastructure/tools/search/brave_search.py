import logging
from typing import Optional
import requests

from src import API_KEYS
from src.infrastructure.tools import run_tool
from src.infrastructure.tools.tools_generator import FunctionToOpenAITool
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatOpenaiGpt35
from src.infrastructure.chat import OpenaiChat

logger = logging.getLogger(__name__)


class BraveSearchTool:
    def __init__(self, api_key: str = API_KEYS.BRAVE_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.base_url = "https://api.search.brave.com/res/v1/{search_type}/search"
        self.headers = {"X-Subscription-Token": api_key, "Accept": "application/json"}
        self.search_kwargs = search_kwargs

    def search(self, query: str, search_type: str = "web", count: int = 10) -> list[dict]:
        """
        This function sends a search request using the provided query and search type, and returns a
        list of search results in JSON format.

        :param query: The `query` parameter is a string that represents the search query that you want
        to send to the API for searching. It is the text or keywords that you want to search for in the
        specified `search_type` (defaulted to "web" if not provided)
        :type query: str
        :param search_type: The `search_type` parameter in the `_search_request` method is used to
        specify the type of search to be performed. By default, it is set to "web", but it can be
        changed to other values such as "image", "video", etc., depending on the available search types
        supported, defaults to web
        :type search_type: str (optional)
        :return: A list of dictionaries containing search results for the given query, specifically from
        the "web" category.
        """
        req = requests.PreparedRequest()
        params = {**self.search_kwargs, **{"q": query, "count": count}}
        req.prepare_url(self.base_url.format(search_type=search_type), params)
        if req.url is None:
            raise ValueError("prepared url is None, this should not happen")

        response = requests.get(req.url, headers=self.headers)
        if not response.ok:
            raise Exception(f"HTTP error {response.status_code}")

        return response.json().get("web", {}).get("results", [])


def search_tool(query: str, search_type: str) -> list[dict]:
    """
    The function `search_with_brave` takes a query and search type as input parameters and returns the result of a search request using the Brave Search API.

    :param query: The `query` parameter is a string that represents the search query that the user wants
    to search for. It could be a keyword, phrase, or question that the user wants to find information
    about
    :type query: str
    :param search_type: The `search_type` parameter specifies the type of search you want to perform. It
    could be something like "web", "images", "videos", "news", etc., depending on the capabilities of
    the search engine you are using
    :type search_type: str
    :return: The function `search_with_brave` is returning the result of a search request made using the
    `brave_search` module, with the specified query and search type.
    """
    search_res = BraveSearchTool().search(query=query, search_type=search_type)
    answer = []
    for res in search_res:
        answer.append(
            {
                "title": res["title"],
                "url": res["url"],
                "description": res["description"],
                "extra_snippets": res.get("extra_snippets"),
                "date": res.get("page_age"),
            }
        )

    return answer


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(search_tool).generate_tool_json()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="how many employees at Deepgram?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    func_res = run_tool(res.tools_call, {"search_tool": search_tool})
    if func_res:
        messages = [
            ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
            ChatMessageSchema(role="user", message="how many employees at Deepgram?"),
            ChatMessageSchema(role="user", message=f"here are some data: {func_res}"),
        ]
        res = OpenaiChat(ChatOpenaiGpt35()).predict(messages)
        print(res)
