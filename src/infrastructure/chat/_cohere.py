import logging
from time import perf_counter

from src import API_KEYS
from src.schemas.message import ChatMessage
from src.utils.markdown_utils import align_markdown_table
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

    def messages_to_cohere_format(self, messages: list[ChatMessage]) -> tuple[str, str, list[ChatMessage]]:
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

    def complete(self, messages: list[dict[str, str]], stream: bool = False) -> Chat_typing:
        if stream:
            raise NotImplementedError("Stream not implemented yet")
        system_message, final_user_message, chat_history = self.messages_to_cohere_format(messages)
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
