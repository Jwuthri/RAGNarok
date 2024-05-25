import logging
from typing import Optional

import serpapi

from src import API_KEYS
from src.infrastructure.tools import run_tool
from src.infrastructure.tools.tools_generator import FunctionToOpenAITool
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatOpenaiGpt35
from src.infrastructure.chat import OpenaiChat

logger = logging.getLogger(__name__)


class GoogleSearchTool:
    def __init__(self, api_key: str = API_KEYS.SERPER_API_KEY, search_kwargs: Optional[dict] = {}) -> None:
        self.client = serpapi.Client(api_key=api_key)

    def search(self, query: str, engine: str = "google") -> list[dict]:
        """
        The function `search` takes a query and an optional search engine parameter, then performs a
        search using the specified search engine and returns the results.

        :param query: The `query` parameter is a string that represents the search query that the user
        wants to search for
        :type query: str
        :param engine: The `engine` parameter in the `search` method specifies the search engine to use
        for the search query. It has a default value of "google" if not specified explicitly, defaults
        to google. Can be ['bing', 'yahoo', 'youtube', 'wallmart', 'ebay', 'duckduckgo', 'google', 'google_autocomplete', 'google_product', 'google_reverse_image', 'google_events', 'google_maps', 'google_images']
        :type engine: str (optional)
        :return: A list of dictionaries containing search results based on the provided query and search
        engine.
        """
        queries_type = {
            "bing": "q",
            "yahoo": "q",
            "youtube": "search_query",
            "wallmart": "query",
            "ebay": "_nkw",
            "duckduckgo": "q",
            "google": "q",
            "google_autocomplete": "q",
            "google_product": "q",
            "google_reverse_image": "image_url",
            "google_events": "q",
            "google_maps": "q",
            "google_images": "q",
        }
        query_type = queries_type.get("engine", "q")
        results = self.client.search({"engine": engine, query_type: query})

        return results


def search_tool(query: str, search_type: str) -> list[dict]:
    """
    The function `search_tool` retrieves search results from Google based on a query and search type,
    and organizes the results into a list of dictionaries containing title, description, question, URL,
    and date information.

    :param query: The `query` parameter is a string that represents the search query you want to perform
    using the search tool. It is the keyword or phrase that you want to search for on the search engine
    :type query: str
    :param search_type: Search type can be "web", "images", "videos", "news", etc. It specifies the type
    of search results you want to retrieve for the given query
    :type search_type: str
    :return: A list of dictionaries containing information such as title, description, question, URL,
    and date related to the search query and type specified.
    """
    search_types = {"news": "google_events", "web": "google", "videos": "youtube", "images": "google_images"}
    search_res = GoogleSearchTool().search(query=query, engine=search_types.get(search_type, "google"))
    answer = []
    for column in ["related_questions", "organic_results"]:
        for res in search_res[column]:
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
