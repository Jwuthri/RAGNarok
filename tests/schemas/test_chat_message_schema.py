import pytest
from src.schemas.chat_message import ChatMessageSchema


def test_chat_message_optional_fields():
    message_text = "Test message"
    role = "system"

    message = ChatMessageSchema(message=message_text, role=role, chat_id="id")

    assert message.meta == {}, "Meta should be None by default."
    assert message.created_at is None, "created_at should be None by default."


def test_chat_message_with_meta():
    message_text = "Test message with meta"
    role = "assistant"
    meta = {"key": "value"}

    message = ChatMessageSchema(message=message_text, role=role, meta=meta, chat_id="id")

    assert message.meta == meta, "Meta should be correctly assigned."


@pytest.mark.parametrize("role", ["system", "user", "assistant"])
def test_chat_message_role_validation(role):
    message = ChatMessageSchema(message="Role validation", role=role, chat_id="id")
    assert message.role == role, "Role should be one of the specified literal values."


def test_chat_message_role_validation_failure():
    with pytest.raises(ValueError):
        ChatMessageSchema(message="Invalid role", role="invalid_role")
