import logging

from src.infrastructure.tokenizer.base import TokenizerManager
from src.schemas.models import ChatModel, ChatOpenaiGpt35


logger = logging.getLogger(__name__)


class OpenaiTokenizer(TokenizerManager):
    def __init__(self, model: ChatModel):
        self.model = model
        try:
            import tiktoken

            self.tokenizer = tiktoken.get_encoding(tiktoken.encoding_for_model(model.name).name)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install tiktoken`")

    def encode(self, text: str):
        return self.tokenizer.encode(text, disallowed_special=())

    def decode(self, tokens: list):
        return self.tokenizer.decode(tokens)

    def length_function(self, text: str) -> int:
        return len(self.tokenizer.encode(text, disallowed_special=()))

    def get_last_n_tokens(self, text: str, n: int = None):
        n = self.model.context_size if not n or n < 0 else n
        tokens = self.encode(text)
        tokens = tokens[-n:] if tokens else tokens

        return "".join(self.decode(tokens))


if __name__ == "__main__":
    res = OpenaiTokenizer(ChatOpenaiGpt35()).length_function("toto")
    logger.info(res)
