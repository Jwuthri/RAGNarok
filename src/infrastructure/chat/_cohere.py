import logging
from time import perf_counter
from typing import Optional

from src import API_KEYS, console, Table
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatCohereCommandR, ChatModel
from src.infrastructure.chat.base import Chat_typing, ChatManager

logger = logging.getLogger(__name__)


class CohereChat(ChatManager):
    def __init__(self, model: ChatModel) -> None:
        self.model = model
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install cohere`")

    def format_message(self, messages: list[ChatMessage]) -> tuple[str, str, list[ChatMessage]]:
        system_message = ""
        final_user_message = ""
        chat_history = []
        roles_mapping = {"system": "Preamble", "user": "User", "assistant": "Chatbot"}
        for i, msg in enumerate(messages):
            if i == 0 and msg.role == "system":
                system_message = msg.message
                continue
            if i == len(messages) - 1:
                final_user_message = msg.message
            else:
                msg.role = roles_mapping[msg.role]
                chat_history.append(msg)

        if len(messages) == 1 and messages[0].role != "system":
            final_user_message = messages[0].message

        return system_message, final_user_message, chat_history

    def complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        system_message, final_user_message, chat_history = self.format_message(messages)
        t0 = perf_counter()
        completion = self.client.chat(
            message=final_user_message,
            preamble=system_message,
            model=self.model.name,
            temperature=self.model.temperature,
            chat_history=chat_history,
        )
        prompt_tokens = completion.token_count.get("prompt_tokens")
        completion_tokens = completion.token_count.get("response_tokens")

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.text,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        system_message, final_user_message, chat_history = self.format_message(messages)
        t0 = perf_counter()
        completion = await self.client.chat(
            message=final_user_message,
            preamble=system_message,
            model=self.model.name,
            temperature=self.model.temperature,
            chat_history=chat_history,
        )
        prompt_tokens = completion.token_count.get("prompt_tokens")
        completion_tokens = completion.token_count.get("response_tokens")

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.text,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("MODEL", justify="left")
        table.add_column("DESCRIPTION", justify="left")
        table.add_column("CONTEXT LENGTH", justify="right")

        table.add_row(
            "command",
            "An instruction-following conversational model that performs language tasks with high quality, more reliably and with a longer context than our base gen",
            "4096",
        )
        table.add_row(
            "command-light", "A smaller, faster version of command. Almost as capable, but a lot faster.", "4096"
        )
        table.add_row(
            "command-nightly",
            "To reduce the time between major releases, we put out nightly versions of command models. For command, that is command-nightly.",
            "8192",
        )
        table.add_row(
            "command-light-nightly",
            "To reduce the time between major releases, we put out nightly versions of command models. For command-light, that is command-light-nightly.",
            "8192",
        )
        table.add_row(
            "command-r",
            "Command R is an instruction-following conversational model that performs language tasks at a higher quality, more reliably,",
            "128000",
        )

        console.print(table)


if __name__ == "__main__":
    CohereChat.describe_models()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant"),
        ChatMessage(role="user", message="what is 5 + 5?"),
    ]
    res = CohereChat(ChatCohereCommandR()).predict(messages)
    logger.info(res)
