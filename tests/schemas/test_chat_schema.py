import pytest
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from src.schemas.chat import ChatSchema


def test_chat_schema_id_generation():
    user_id = "user123"
    thread_id = "thread456"
    meta = {"example": "data"}

    chat = ChatSchema(user_id=user_id, thread_id=thread_id, meta=meta)

    expected_id = str(uuid5(NAMESPACE_DNS, f"{user_id}:{thread_id}:{meta}"))
    assert chat.id == expected_id


def test_chat_schema_optional_fields():
    chat = ChatSchema()

    assert chat.meta is None, "Meta should be None by default."
    assert chat.user_id is None, "user_id should be None by default."
    assert chat.thread_id is None, "thread_id should be None by default."
    assert chat.assistant_id is None, "assistant_id should be None by default."
    assert chat.created_at is None, "created_at should be None by default."
    assert chat.updated_at is None, "updated_at should be None by default."


def test_chat_schema_with_timestamps():
    now = datetime.now()

    chat = ChatSchema(created_at=now, updated_at=now)

    assert chat.created_at == now, "created_at should match the provided datetime."
    assert chat.updated_at == now, "updated_at should match the provided datetime."


@pytest.mark.parametrize("meta", [{}, {"key": "value"}])
def test_chat_schema_with_meta(meta):
    chat = ChatSchema(meta=meta)

    assert chat.meta == meta
