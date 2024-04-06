import pytest
from datetime import datetime
from pydantic import ValidationError

from src.schemas.chat_history import ChatHistorySchema


def test_chat_history_schema():
    """
    Test case for ChatHistorySchema class.
    """
    # Valid data
    valid_data = {
        "chat_message_id": "message_id",
        "chat_id": "chat_id",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "meta": {"key": "value"},
        "prompt_id": "prompt_id",
    }

    # Test valid data
    chat_history = ChatHistorySchema(**valid_data)
    assert chat_history.id is not None
    assert chat_history.chat_message_id == valid_data["chat_message_id"]
    assert chat_history.meta == valid_data["meta"]
    assert chat_history.chat_id == valid_data["chat_id"]
    assert chat_history.prompt_id == valid_data["prompt_id"]
    assert chat_history.created_at == valid_data["created_at"]
    assert chat_history.updated_at == valid_data["updated_at"]

    # Test invalid data (missing required field)
    invalid_data = {
        "chat_id": "chat_id",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "meta": {"key": "value"},
        "prompt_id": "prompt_id",
    }
    with pytest.raises(ValidationError):
        chat_history = ChatHistorySchema(**invalid_data)
