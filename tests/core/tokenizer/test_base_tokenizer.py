import pytest

from src.core.tokenizer import TokenizerManager
from src.schemas.models import ChatModel


@pytest.fixture
def tokenizer():
    return TokenizerManager(
        model=ChatModel(
            name="name", max_output=1024, context_size=1024, cost_prompt_token=0.0, cost_completion_token=0.0
        )
    )


def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


def test_encode(tokenizer):
    assert tokenizer.encode("hi text") == ["hi", "text"]
