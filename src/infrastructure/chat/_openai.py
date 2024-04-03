import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS
from src.schemas.chat_message import ChatMessage
from src.utils.markdown_utils import align_markdown_table
from src.schemas.models import ChatCohereCommandR, ChatModel
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

    def messages_to_openai_format(self, messages: list[ChatMessage]) -> list[dict[str, str]]:
        chat_history = []
        roles_mapping = {"system": "system", "user": "user", "assistant": "assistant"}
        for _, msg in enumerate(messages):
            chat_history.append({"role": roles_mapping[msg.role], "content": msg.message})

        return chat_history

    def complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.messages_to_openai_format(messages=messages)
        completion = self.client.chat.completions.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            frequency_penalty=self.model.frequency_penalty,
            presence_penalty=self.model.presence_penalty,
            stop=self.model.stop,
            response_format=response_format,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.text,
            model_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: bool = False
    ) -> Chat_typing:
        t0 = perf_counter()
        formatted_messages = self.messages_to_openai_format(messages=messages)
        completion = await self.client.chat.completions.create(
            model=self.model.name,
            messages=formatted_messages,
            max_tokens=self.model.max_output,
            temperature=self.model.temperature,
            frequency_penalty=self.model.frequency_penalty,
            presence_penalty=self.model.presence_penalty,
            stop=self.model.stop,
            response_format=response_format,
        )
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens

        return Chat_typing(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.text,
            model_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | LATEST MODEL          | DESCRIPTION                                                                                                                                             | MAX TOKENS (CONTEXT LENGTH) | ENDPOINTS       |
            |-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|-----------------|
            | command               | An instruction-following conversational model that performs language tasks with high quality, more reliably and with a longer context than our base gen | 4096                        | Chat, Summarize |
            | command-light         | A smaller, faster version of command. Almost as capable, but a lot faster.                                                                              | 4096                        | Chat, Summarize |
            | command-nightly       | To reduce the time between major releases, we put out nightly versions of command models. For command, that is command-nightly.                         | 8192                        | Chat            |
            | command-light-nightly | To reduce the time between major releases, we put out nightly versions of command models. For command-light, that is command-light-nightly.             | 8192                        | Chat            |
            | command-r             | Command R is an instruction-following conversational model that performs language tasks at a higher quality, more reliably,                             | 128000                      | Chat            |
            """
            )
        )


if __name__ == "__main__":
    CohereChat.describe_models()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant"),
        ChatMessage(role="user", message="what is 5 + 5?"),
    ]
    res = CohereChat(ChatCohereCommandR()).predict(messages, False)
    logger.info(res)
