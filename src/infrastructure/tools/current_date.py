import logging
from datetime import date

from src.infrastructure.tools.base import FunctionToOpenAITool
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatOpenaiGpt35
from src.infrastructure.chat import OpenaiChat

logger = logging.getLogger(__name__)


def get_current_date(city: str) -> str:
    """
    The function `get_current_date` returns the current date, but it seems to be missing an import
    statement for the `date` module.

    :param city: It looks like you are trying to create a function that returns the current date for a
    given city. However, the implementation you provided is returning the `date.today()` object
    directly, which may not be what you intended
    :type city: str
    :return: The function is supposed to return the current date as a string. However, the current
    implementation is returning a `date` object instead of a string.
    """
    return date.today()


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(get_current_date).generate_tool_json()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessage(role="user", message="what is the time here?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    logger.info(res)
