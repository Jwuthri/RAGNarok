import logging

from src.infrastructure.tokenizer.base import TokenizerManager
from src import API_KEYS
from src.schemas.models import ChatAnthropicClaude12, ChatModel

logger = logging.getLogger(__name__)


class AnthropicTokenizer(TokenizerManager):
    def __init__(self, model: ChatModel):
        self.model = model
        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=API_KEYS.ANTHROPIC_API_KEY)
            self.tokenizer = self.client.get_tokenizer()
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install tiktoken`")

    def encode(self, text: str):
        return self.tokenizer.encode(text)

    def decode(self, tokens: list):
        raise NotImplementedError()

    def length_function(self, text: str) -> int:
        return len(self.encode(text).ids)

    def get_last_n_tokens(self, text: str, n: int = None):
        n = self.model.context_size if not n or n < 0 else n
        tokens = self.encode(text)
        tokens = tokens[-n:] if tokens else tokens

        return "".join(self.decode(tokens))


if __name__ == "__main__":
    res = AnthropicTokenizer(ChatAnthropicClaude12()).encode("hi test")
    logger.info(res)
    breakpoint()
