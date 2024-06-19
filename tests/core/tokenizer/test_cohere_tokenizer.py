import pytest

from src.schemas.models import ChatCohereCommandR
from src.core.tokenizer import CohereTokenizer


@pytest.fixture
def tokenizer():
    return CohereTokenizer(ChatCohereCommandR())


@pytest.mark.skip("require api key")
def test_length_function(tokenizer):
    assert tokenizer.length_function("hi text") == 2


@pytest.mark.skip("require api key")
def test_encode(tokenizer):
    assert tokenizer.encode("hi text") == [5649, 4518]
