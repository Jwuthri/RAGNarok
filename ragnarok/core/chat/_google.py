import logging
from typing import Optional
from time import perf_counter

from ragnarok import API_KEYS, console
from ragnarok.schemas.chat_message import ChatMessageSchema
from ragnarok.schemas.models import ChatModel, ChatGoogleGeminiPro1, google_table
from ragnarok.core.chat.base import PromptSchema, ChatManager

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
            logger.warning("Please run `pip install google-generativeai`")

    def format_message(self, messages: list[ChatMessageSchema]) -> str:
        return "\n".join([msg.message for msg in messages])

    @property
    def model_config(self):
        return {"temperature": self.model.temperature, "max_output_tokens": self.model.max_output}

    def complete(
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        model = self.client.GenerativeModel(model_name=self.model.name, generation_config=self.model_config)
        chat = model.start_chat(history=[])
        completion = chat.send_message(formatted_messages)
        prompt_tokens = model.count_tokens(formatted_messages).total_tokens
        completion_tokens = model.count_tokens(completion.text).total_tokens

        return PromptSchema(
            prompt=[message.model_dump() for message in messages],
            prediction=completion.text,
            llm_name=self.model.name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=prompt_tokens * self.model.cost_prompt_token + completion_tokens * self.model.cost_completion_token,
            latency=perf_counter() - t0,
        )

    async def a_complete(
        self, messages: list[ChatMessageSchema], response_format: Optional[str] = None, stream: bool = False
    ) -> PromptSchema:
        t0 = perf_counter()
        formatted_messages = self.format_message(messages=messages)
        model = self.client.GenerativeModel(model_name=self.model.name, generation_config=self.model_config)
        chat = model.start_chat(history=[])
        completion = chat.send_message(formatted_messages)
        prompt_tokens = model.count_tokens(formatted_messages).total_tokens
        completion_tokens = model.count_tokens(completion.text).total_tokens

        return PromptSchema(
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
        console.print(google_table)


if __name__ == "__main__":
    GoogleChat.describe_models()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessageSchema(role="user", message="what is 5 + 5?"),
    ]
    res = GoogleChat(ChatGoogleGeminiPro1()).predict(messages)
    logger.info(res)
