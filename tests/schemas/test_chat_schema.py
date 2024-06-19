import pytest
from datetime import datetime

from src.schemas.chat import ChatSchema


def test_chat_schema_id_generation():
    thread_id = "thread456"
    meta = {"example": "data"}

    chat = ChatSchema(thread_id=thread_id, meta=meta)

    assert chat.id == "de267bf7-4988-5483-9ce9-17562922da1d"


def test_chat_schema_optional_fields():
    chat = ChatSchema()

    assert chat.meta == {}, "Meta should be None by default."
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
