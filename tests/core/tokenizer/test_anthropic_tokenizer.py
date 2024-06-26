import pytest

from ragnarok.schemas.models import ChatAnthropicClaude12
from ragnarok.core.tokenizer import AnthropicTokenizer


@pytest.fixture
def tokenizer():
    return AnthropicTokenizer(ChatAnthropicClaude12())


def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


def test_encode(tokenizer):
    assert tokenizer.encode("hi text").ids == [5630, 1373]
