import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from src.schemas.chat_message import ChatMessageSchema
from src.repositories.chat_message import ChatMessageRepository


@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked database session."""
    return create_autospec(Session, instance=True, spec_set=True)


@pytest.fixture
def chat_message_data():
    """Provides a sample ChatMessage data for testing."""
    return ChatMessageSchema(
        message="Test message", role="user", meta={"sample": "data"}, created_at=datetime.now(), chat_id="id"
    )


def test_create_chat_message(mock_db_session, chat_message_data):
    """Test the create method of ChatMessageRepository."""
    repository = ChatMessageRepository(mock_db_session)
    repository.create(chat_message_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
