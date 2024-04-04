import logging
from typing import Optional
from time import perf_counter

from src import API_KEYS, console, Table
from src.schemas.chat_message import ChatMessage
from src.schemas.models import ChatModel, ChatAnthropicClaude12
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
        self, messages: list[ChatMessage], response_format: Optional[str] = None, stream: bool = False
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
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("MODEL", justify="left")
        table.add_column("DESCRIPTION", justify="left")
        table.add_column("STRENGTHS", justify="left")
        table.add_column("MULTILINGUAL", justify="center")
        table.add_column("VISION", justify="center")
        table.add_column("LATEST API MODEL NAME", justify="left")
        table.add_column("API FORMAT", justify="left")
        table.add_column("COMPARATIVE LATENCY", justify="left")
        table.add_column("CONTEXT WINDOW", justify="left")
        table.add_column("MAX OUTPUT", justify="right")
        table.add_column("COST (Input / Output per MTok)", justify="left")
        table.add_column("TRAINING DATA CUT-OFF", justify="left")

        # Adding rows with the Claude model data
        table.add_row(
            "Claude 3 Opus",
            "Most powerful model for highly complex tasks",
            "Top-level performance, intelligence, fluency, and understanding",
            "Yes",
            "Yes",
            "claude-3-opus-20240229",
            "Messages API",
            "Moderately fast",
            "200K*",
            "4096 tokens",
            "$15.00 / $75.00",
            "Aug 2023",
        )
        table.add_row(
            "Claude 3 Sonnet",
            "Ideal balance of intelligence and speed for enterprise workloads",
            "Maximum utility at a lower price, dependable, balanced for scaled deployments",
            "Yes",
            "Yes",
            "claude-3-sonnet-20240229",
            "Messages API",
            "Fast",
            "200K*",
            "4096 tokens",
            "$3.00 / $15.00",
            "Aug 2023",
        )
        table.add_row(
            "Claude 3 Haiku",
            "Fastest and most compact model for near-instant responsiveness",
            "Quick and accurate targeted performance",
            "Yes",
            "Yes",
            "claude-3-haiku-20240307",
            "Messages API",
            "Fastest",
            "200K*",
            "4096 tokens",
            "$0.25 / $1.25",
            "Aug 2023",
        )
        table.add_row(
            "Claude 2.1",
            "Updated version of Claude 2 with improved accuracy",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-2.1",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "200K*",
            "4096 tokens",
            "$8.00 / $24.0",
            "Early 2023",
        )
        table.add_row(
            "Claude 2",
            "Predecessor to Claude 3, offering strong all-round performance",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-2.0",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "100K**",
            "4096 tokens",
            "$8.00 / $24.0",
            "Early 2023",
        )
        table.add_row(
            "Claude Instant 1.2",
            "Our cheapest small and fast model, a predecessor of Claude Haiku.",
            "Legacy model - performs less well than Claude 3 models",
            "Yes, with less coverage, understanding, and skill than Claude 3",
            "No",
            "claude-instant-1.2",
            "Messages & Text Completions API",
            "Slower than Claude 3 model of similar intelligence",
            "100K**",
            "4096 tokens",
            "$0.80 / $2.40",
            "Early 2023",
        )

        console.print(table)


if __name__ == "__main__":
    AnthropicChat.describe_models()
    messages = [
        ChatMessage(role="system", message="You are an ai assistant, always response as json format"),
        ChatMessage(role="user", message="what is 5 + 5?"),
    ]
    res = AnthropicChat(ChatAnthropicClaude12()).predict(messages)
    logger.info(res)
