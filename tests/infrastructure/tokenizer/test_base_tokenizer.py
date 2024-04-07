import pytest

from src.infrastructure.tokenizer import TokenizerManager


@pytest.fixture
def tokenizer():
    return TokenizerManager()


def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


def test_encode(tokenizer):
    assert tokenizer.encode("hi text") == ["hi", "text"]
