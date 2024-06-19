from ragnarok.core.tools.tools_generator import FunctionToOpenAITool
from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.models import ChatOpenaiGpt35
from ragnarok.core.chat import OpenaiChat
from ragnarok.core.tools import run_tool


def router(query: str, query_type: str):
    """
    determine which type of query it is. Should it return a 'slide', 'image', 'video', 'search', 'answer'.

    :param query: The `query` parameter is a string that represents the query being passed to the
    router function. In this case, the function is designed to handle queries related to images
    :type query: str
    :param query_type: query_type is a parameter that specifies the type of query being passed to
    the router function. In this case, it is a string indicating whether the query is 'slide', 'image', 'video', 'search', 'answer'
    :type query_type: str
    """
    match query_type:
        case "image":
            return query
        case "video":
            return query
        case "search":
            return query
        case "slide":
            return query
        case _:
            return query


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(router).generate_tool_json()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(
            role="user", message="how does split compare to launchdarkly? do you have an image of a cat?"
        ),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tools_call, {"router": router})
    print(func_res)
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="create a presentation about split security"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tools_call, {"router": router})
    print(func_res)
