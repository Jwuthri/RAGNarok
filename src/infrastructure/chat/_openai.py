import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS, CONSOLE, Table
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatModel, ChatOpenaiGpt35
from src.infrastructure.chat.base import Chat_typing, ChatManager

logger = logging.getLogger(__name__)


class OpenaiChat(ChatManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        self.model = model
        try:
            from openai import OpenAI, AsyncOpenAI

            if sync:
                self.client = OpenAI(api_key=API_KEYS.OPENAI_API_KEY)
            else:
                self.client = AsyncOpenAI(api_key=API_KEYS.OPENAI_API_KEY)
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install openai`")

    def format_message(self, messages: list[ChatMessage]) -> list[dict[str, str]]:
        chat_history = []
        roles_mapping = {"system": "system", "user": "user", "assistant": "assistant"}
        for _, msg in enumerate(messages):
            chat_history.append({"role": roles_mapping[msg.role], "content": msg.message})

        return chat_history

    def complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        completion = self.client.chat.completions.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            frequency_penalty=self.model.frequency_penalty,
            presence_penalty=self.model.presence_penalty,
            stop=self.model.stop,
            response_format={"type": response_format} if response_format else None,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.choices[0].message.content,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: bool = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        completion = await self.client.chat.completions.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            frequency_penalty=self.model.frequency_penalty,
            presence_penalty=self.model.presence_penalty,
            stop=self.model.stop,
            response_format={"type": response_format} if response_format else None,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.choices[0].message.content,
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
            "gpt-4-0125-preview", "New GPT-4 Turbo intended to reduce 'laziness'.", "128,000 tokens / Up to Dec 2023"
        )
        table.add_row("gpt-4-turbo-preview", "Points to gpt-4-0125-preview.", "128,000 tokens / Up to Dec 2023")
        table.add_row(
            "gpt-4-1106-preview",
            "Features improved instruction following, JSON mode, and more.",
            "128,000 tokens / Up to Apr 2023",
        )
        table.add_row(
            "gpt-4-vision-preview", "GPT-4 with image understanding capabilities.", "128,000 tokens / Up to Apr 2023"
        )
        table.add_row("gpt-4", "Currently points to gpt-4-0613.", "8,192 tokens / Up to Sep 2021")
        table.add_row(
            "gpt-3.5-turbo-0125", "Latest GPT-3.5 Turbo model with higher accuracy.", "16,385 tokens / Up to Sep 2021"
        )
        table.add_row("gpt-3.5-turbo", "Points to gpt-3.5-turbo-0125.", "16,385 tokens / Up to Sep 2021")
        table.add_row(
            "gpt-3.5-turbo-instruct",
            "Similar capabilities as GPT-3 models, for legacy endpoints.",
            "4,096 tokens / Up to Sep 2021",
        )
        CONSOLE.print(table)


if __name__ == "__main__":
    OpenaiChat.describe_models()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessage(role="user", message="what is 5 + 5?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages)
    logger.info(res)
