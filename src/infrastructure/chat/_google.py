import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS, CONSOLE, Table
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatModel, ChatGoogleGeminiPro1
from src.infrastructure.chat.base import Chat_typing, ChatManager

logger = logging.getLogger(__name__)


class GoogleChat(ChatManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        self.model = model
        try:
            import google.generativeai as genai

            self.client = genai
            self.client.configure(api_key=API_KEYS.GOOGLE_API_KEY)
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install -U google-generativeai`")

    def format_message(self, messages: list[ChatMessage]) -> str:
        return "\n".join([msg.message for msg in messages])

    @property
    def model_config(self):
        return {"temperature": self.model.temperature, "max_output_tokens": self.model.max_output}

    def complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        model = self.client.GenerativeModel(model_name=self.model.name, generation_config=self.model_config)
        chat = model.start_chat(history=[])
        completion = chat.send_message(formatted_messages)
        prompt_tokens = model.count_tokens(formatted_messages).total_tokens
        completion_tokens = model.count_tokens(completion.text).total_tokens

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
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: bool = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        model = self.client.GenerativeModel(model_name=self.model.name, generation_config=self.model_config)
        chat = model.start_chat(history=[])
        completion = chat.send_message(formatted_messages)
        prompt_tokens = model.count_tokens(formatted_messages).total_tokens
        completion_tokens = model.count_tokens(completion.text).total_tokens

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
    GoogleChat.describe_models()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessage(role="user", message="what is 5 + 5?"),
    ]
    res = GoogleChat(ChatGoogleGeminiPro1()).predict(messages)
    logger.info(res)
