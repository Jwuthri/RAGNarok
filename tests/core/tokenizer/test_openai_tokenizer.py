import pytest

from ragnarok.schemas.models import ChatOpenaiGpt35
from ragnarok.core.tokenizer import OpenaiTokenizer


@pytest.fixture
def tokenizer():
    return OpenaiTokenizer(ChatOpenaiGpt35())


def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


def test_encode(tokenizer):
    assert tokenizer.encode("hi text") == [6151, 1495]
