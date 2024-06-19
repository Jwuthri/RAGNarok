import logging

from src.core.tokenizer.base import TokenizerManager
from src import API_KEYS
from src.schemas.models import ChatCohereCommandR, ChatModel

logger = logging.getLogger(__name__)


class CohereTokenizer(TokenizerManager):
    def __init__(self, model: ChatModel):
        self.model = model
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
            self.tokenizer = self.client.tokenize
            self.detokenizer = self.client.detokenize
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def encode(self, text: str):
        return self.tokenizer(text=text, model=self.model.name).tokens

    def decode(self, tokens: list):
        raise self.detokenizer(tokens=tokens, model=self.model.name)

    def length_function(self, text: str) -> int:
        return len(self.encode(text))

    def get_last_n_tokens(self, text: str, n: int = None):
        n = self.model.context_size if not n or n < 0 else n
        tokens = self.encode(text)
        tokens = tokens[-n:] if tokens else tokens

        return "".join(self.decode(tokens))


if __name__ == "__main__":
    res = CohereTokenizer(ChatCohereCommandR()).encode("hi test")
    logger.info(res)
