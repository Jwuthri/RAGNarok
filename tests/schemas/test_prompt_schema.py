import pytest
from datetime import datetime
from pydantic import ValidationError

from src.schemas.prompt import PromptSchema
from src.schemas.chat_message import ChatMessageSchema


def test_prompt_schema():
    """
    Test case for PromptSchema class.
    """
    # Valid data
    valid_data = {
        "cost": 10.5,
        "latency": 0.5,
        "llm_name": "example_llm",
        "prediction": "some_prediction",
        "prompt_tokens": 5,
        "completion_tokens": 10,
        "prompt": [{"message": "Hello", "role": "user"}],
        "meta": {"key": "value"},
        "created_at": datetime.now(),
    }

    # Test valid data
    prompt_schema = PromptSchema(**valid_data)
    assert prompt_schema.id is not None
    assert prompt_schema.cost == valid_data["cost"]
    assert prompt_schema.latency == valid_data["latency"]
    assert prompt_schema.llm_name == valid_data["llm_name"]
    assert prompt_schema.prediction == valid_data["prediction"]
    assert prompt_schema.tools_call == {}
    assert prompt_schema.prompt_tokens == valid_data["prompt_tokens"]
    assert prompt_schema.completion_tokens == valid_data["completion_tokens"]
    assert prompt_schema.meta == valid_data["meta"]
    assert prompt_schema.created_at == valid_data["created_at"]
    # Test invalid data (missing required field)
    invalid_data = {
        "cost": 10.5,
        "latency": 0.5,
        "llm_name": "example_llm",
        "prompt_tokens": 5,
        "prompt": [{"message": "Hello", "sender": "user"}],
        "meta": {"key": "value"},
        "created_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        prompt_schema = PromptSchema(**invalid_data)
