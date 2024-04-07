import pytest
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from src.schemas.chat_message import ChatMessage


def test_chat_message_id_generation():
    message_text = "Hello, World!"
    role = "user"
    created_at = datetime(2022, 1, 1, 12, 0, 0)

    message = ChatMessage(message=message_text, role=role, created_at=created_at)

    expected_id = str(uuid5(NAMESPACE_DNS, f"{role}:{message_text}:{created_at}"))
    assert message.id == expected_id, "The ID should be generated correctly based on role, message, and created_at."


def test_chat_message_optional_fields():
    message_text = "Test message"
    role = "system"

    message = ChatMessage(message=message_text, role=role)

    assert message.meta is None, "Meta should be None by default."
    assert message.created_at is None, "created_at should be None by default."


def test_chat_message_with_meta():
    message_text = "Test message with meta"
    role = "assistant"
    meta = {"key": "value"}

    message = ChatMessage(message=message_text, role=role, meta=meta)

    assert message.meta == meta, "Meta should be correctly assigned."


@pytest.mark.parametrize("role", ["system", "user", "assistant"])
def test_chat_message_role_validation(role):
    message = ChatMessage(message="Role validation", role=role)
    assert message.role == role, "Role should be one of the specified literal values."


def test_chat_message_role_validation_failure():
    with pytest.raises(ValueError):
        ChatMessage(message="Invalid role", role="invalid_role")
