import pytest

from src.schemas.models import ChatCohereCommandR
from src.infrastructure.tokenizer import CohereTokenizer


@pytest.fixture
def tokenizer():
    return CohereTokenizer(ChatCohereCommandR())


def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


def test_encode(tokenizer):
    assert tokenizer.encode("hi text") == [5649, 4518]
