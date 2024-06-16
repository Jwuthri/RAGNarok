import logging
from time import perf_counter
from typing import Optional

from src import API_KEYS, console
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatCohereCommandRPlus, ChatModel, cohere_table
from src.infrastructure.chat.base import PromptSchema, ChatManager

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

    def format_message(self, messages: list[ChatMessageSchema]) -> tuple[str, str, list[ChatMessageSchema]]:
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
        self,
        messages: list[ChatMessageSchema],
        response_format: Optional[str] = None,
        stream: Optional[bool] = False,
        tools: Optional[list] = None,
    ) -> PromptSchema:
        system_message, final_user_message, chat_history = self.format_message(messages)
        t0 = perf_counter()
        completion = self.client.chat(
            message=final_user_message,
            preamble=system_message,
            model=self.model.name,
            temperature=self.model.temperature,
            chat_history=chat_history,
        )
        prompt_tokens = completion.meta["tokens"].get("input_tokens")
        completion_tokens = completion.meta["tokens"].get("output_tokens")

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
        self, messages: list[ChatMessageSchema], response_format: Optional[str] = None, stream: Optional[bool] = False
    ) -> PromptSchema:
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
        console.print(cohere_table)


if __name__ == "__main__":
    CohereChat.describe_models()
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessageSchema(role="user", message="what is 5 + 5?"),
    ]
    res = CohereChat(ChatCohereCommandRPlus()).predict(messages)
    logger.info(res)
