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


class ScrapperSerperTool:
    def __init__(self, api_key: str = API_KEYS.GOOGLE_SERPER_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    def search(self, url: str) -> list[dict]:
        """
        The function sends a POST request to "google.serper.dev" with a JSON payload containing a URL
        and returns the response data as a decoded string.

        :param url: The `url` parameter in the `search` function is a string that represents the URL you
        want to search for on the specified server
        :type url: str
        :return: The code is currently returning the response data from the HTTP request as a decoded
        string in UTF-8 format.
        """
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"url": url})
        conn.request("POST", "/", payload, self.headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")


def scrapper_tool(url: str) -> list[dict]:
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
    func_res = run_tool(res.tool_call, {"scrapper_tool": scrapper_tool})
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
