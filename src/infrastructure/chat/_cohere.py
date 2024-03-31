import logging

from src.infrastructure.chat.base import ChatManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class CohereChat(ChatManager):
    def __init__(self, model_name: str = "command-r", temperature: float = 0.0) -> None:
        self.model_name = model_name
        self.temperature = temperature
        try:
            import cohere

            self.client = cohere.Client("{apiKey}")
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def complete(self, system: str, message: str, stream: bool):
        return self.client.chat(
            message=message, preamble=system, model=self.model_name, temperature=self.temperature, stream=stream
        )

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
    x = CohereChat()
    x.describe_models()
