import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS, console
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatModel, ChatOpenaiGpt35, openai_table
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
        completion = self.client.chat.completions.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            frequency_penalty=self.model.frequency_penalty,
            presence_penalty=self.model.presence_penalty,
            stop=self.model.stop,
            response_format={"type": response_format} if response_format else None,
            tool_choice="auto" if tools else None,
            tools=tools,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.choices[0].message.content,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            tools_call=[x.model_dump() for x in completion.choices[0].message.tool_calls]
            if completion.choices[0].message.tool_calls
            else None,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: bool = False,
        tools: Optional[list] = None,
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
            tool_choice="auto" if tools else None,
            tools=tools,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.choices[0].message.content,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            tools_call=[x.model_dump() for x in completion.choices[0].message.tool_calls]
            if completion.choices[0].message.tool_calls
            else None,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    @classmethod
    def describe_models(self):
        console.print(openai_table)


if __name__ == "__main__":
    OpenaiChat.describe_models()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessageSchema(role="user", message="what is 5 + 5?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages)
    logger.info(res)
