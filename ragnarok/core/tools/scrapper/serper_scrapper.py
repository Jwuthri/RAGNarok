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


class ScrapperSerperTool:
    def __init__(self, api_key: str = API_KEYS.GOOGLE_SERPER_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        self.base_url = "https://scrape.serper.dev"
        self.search_kwargs = search_kwargs

    def search(self, url: str) -> dict:
        """
        The function sends a POST request to "google.serper.dev" with a JSON payload containing a URL
        and returns the response data as a decoded string.

        :param url: The `url` parameter in the `search` function is a string that represents the URL you
        want to search for on the specified server
        :type url: str
        :return: The code is currently returning the response data from the HTTP request as a decoded
        string in UTF-8 format.
        """
        payload = json.dumps({"url": url})
        response = requests.request("POST", self.base_url, headers=self.headers, data=payload)

        return response.json()


def scrapper_tool(url: str) -> dict:
    """
    The function `scrapper_tool` takes a URL as input and returns a list of dictionaries containing
    search results obtained using a ScrapperSerperTool.

    :param url: The `url` parameter in the `scrapper_tool` function is a string that represents the URL
    of the website that you want to scrape data from
    :type url: str
    :return: A list of dictionaries containing the search results obtained by using the
    ScrapperSerperTool to search the provided URL.
    """
    search_res = ScrapperSerperTool().search(url=url)

    return search_res


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(scrapper_tool).generate_tool_json()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="how many employees at Deepgram in 2024?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    logger.info(res)
    func_res = run_tool(res.tools_call, {"scrapper_tool": scrapper_tool})
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
