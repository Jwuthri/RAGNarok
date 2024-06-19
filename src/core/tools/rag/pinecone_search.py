from typing import Optional

from src import API_KEYS
from src.core.tools import run_tool
from src.core.tools.tools_generator import FunctionToOpenAITool
from src.core.text_embedding import OpenaiEmbedding, EmbeddingManager
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatOpenaiGpt35, EmbeddingOpenaiSmall3, ChatOpenaiGpt4Turbo
from src.core.chat import OpenaiChat
from src.core.vector_stores import PineconeVectorStore


class PineconeSearchTool:
    def __init__(self, embedding: EmbeddingManager = OpenaiEmbedding(EmbeddingOpenaiSmall3())) -> None:
        self.store = PineconeVectorStore(embedding=embedding)

    def search(
        self, query: str, namespace: str, count: int = 10, index_name: str = API_KEYS.PINECONE_INDEX
    ) -> list[dict]:
        """
        This function searches for a specified query within a given namespace using Pinecone indexing
        and returns a list of results.

        :param query: The `query` parameter is a string that represents the search query that you want
        to perform in the specified namespace within the given index. It is used to search for relevant
        items based on the provided query string
        :type query: str
        :param namespace: The `namespace` parameter in the `search` method refers to the specific
        namespace within which you want to search for results. Namespaces are used to organize and group
        data within an index, allowing you to perform searches within a specific subset of data rather
        than the entire index. When calling the `search
        :type namespace: str
        :param count: The `count` parameter in the `search` method specifies the number of results that
        should be returned by the search query. By default, it is set to 10, meaning that the method
        will return up to 10 results unless specified otherwise when calling the method, defaults to 10
        :type count: int (optional)
        :param index_name: The `index_name` parameter specifies the name of the index to search within.
        In the provided code snippet, the default value for `index_name` is `API_KEYS.PINECONE_INDEX`.
        This parameter allows you to specify the specific index within which you want to perform the
        search operation
        :type index_name: str
        :return: The `search` method is returning a list of dictionaries.
        """
        return self.store.query(index_name=index_name, query=query, top_k=count, namespace=namespace)


def retriever_tool(query: str, namespace: str) -> list[dict]:
    """
    The `retriever_tool` function retrieves search results about deepgram using a specified query and namespace, it knows information about deepgram.

    :param query: The `query` parameter is a string that represents the search query you want to use to retrieve data from the specified namespace
    :type query: str
    :param namespace: The `namespace` parameter refers to a specific index, it can be "fuds-alert", "roadmap", "images", "videos" or "deepgram|deepgram|72599065905526311|2024-05-03-09-29-20".
    :type namespace: str
    :return: A list of dictionaries containing search results for the given query within the specified
    namespace.
    """
    search_res = PineconeSearchTool().search(query=query, namespace=namespace).to_dict()
    if "matches" in search_res:
        return search_res["matches"]

    return None


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(retriever_tool).generate_tool_json()
    messages = [
        ChatMessageSchema(
            role="system", message="You are an ai assistant to answer question about deepgram, Use tools when you can"
        ),
        ChatMessageSchema(role="user", message="Where is paris?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt4Turbo()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tools_call, {"retriever_tool": retriever_tool})
    # print(func_res)
    messages = [
        ChatMessageSchema(
            role="system", message="You are an ai assistant to answer question about deepgram, Use tools when you can"
        ),
        ChatMessageSchema(role="user", message="What is the accuracy of your detection?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt4Turbo()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tools_call, {"retriever_tool": retriever_tool})
    # print(func_res)
    if func_res:
        messages = [
            ChatMessageSchema(
                role="system",
                message="You are an ai assistant to answer question about deepgram, Use tools when you can",
            ),
            ChatMessageSchema(role="user", message="What is the accuracy of your detection?"),
            ChatMessageSchema(role="user", message=f"here are some information: {func_res}"),
        ]
        res = OpenaiChat(ChatOpenaiGpt4Turbo()).predict(messages)
        print(res)
