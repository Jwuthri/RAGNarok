import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS, console, Table
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatAnthropicClaude12, anthropic_table
from src.infrastructure.chat.base import Chat_typing, ChatManager

logger = logging.getLogger(__name__)


class AnthropicChat(ChatManager):
    def __init__(self, model: ChatModel, sync: Optional[bool] = True) -> None:
        self.model = model
        try:
            from anthropic import Anthropic, AsyncAnthropic

            if sync:
                self.client = Anthropic(api_key=API_KEYS.ANTHROPIC_API_KEY)
            else:
                self.client = AsyncAnthropic(api_key=API_KEYS.ANTHROPIC_API_KEY)
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install anthropic`")

    def format_message(self, messages: list[ChatMessageSchema]) -> list[dict[str, str]]:
        chat_history = []
        roles_mapping = {"system": "system", "user": "user", "assistant": "assistant"}
        for _, msg in enumerate(messages):
            chat_history.append({"role": roles_mapping[msg.role], "content": msg.message})

        return chat_history

    def complete(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        system = ""
        for i, message in enumerate(formatted_messages):
            if message["role"] == "system":
                system = formatted_messages.pop(i)["content"]

        completion = self.client.messages.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            stop_sequences=self.model.stop,
            system=system,
        )
        prompt_tokens = completion.usage.input_tokens
        completion_tokens = completion.usage.output_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.content[0].text,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self, messages: list[ChatMessageSchema], response_format: Optional[str] = None, stream: bool = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        system = ""
        for i, message in enumerate(formatted_messages):
            if message["role"] == "system":
                system = formatted_messages.pop(i)["content"]
        completion = await self.client.messages.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            stop_sequences=self.model.stop,
            system=system,
        )
        prompt_tokens = completion.usage.input_tokens
        completion_tokens = completion.usage.output_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.content[0].text,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    @classmethod
    def describe_models(self):
        console.print(anthropic_table)


if __name__ == "__main__":
    AnthropicChat.describe_models()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessageSchema(role="user", message="what is 5 + 5?"),
    ]
    res = AnthropicChat(ChatAnthropicClaude12()).predict(messages)
    logger.info(res)
