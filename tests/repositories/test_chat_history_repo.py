import pytest
from datetime import datetime
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from src.repositories.chat_history import ChatHistoryRepository
from src.db.chat_history import ChatHistoryTable
from src.schemas.chat_history import ChatHistorySchema


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mocked database session.
    """
    return create_autospec(Session, instance=True, spec_set=True)


mock_data = {
    "chat_id": "chat123",
    "chat_message_id": "toto",
    "created_at": datetime.now(),
}
mock_record = ChatHistorySchema(**mock_data)


def test_create_chat_history(mock_db_session):
    db_record = ChatHistoryTable(**mock_data)

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.query.return_value.first.return_value = db_record

    repository = ChatHistoryRepository(mock_db_session)
    result = repository.create(mock_record)

    assert result == mock_record
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_read_chat_history_exists(mock_db_session):
    mock_db_session.query(ChatHistoryTable).filter(
        ChatHistoryTable.id == mock_record.id
    ).first.return_value = mock_record
    repository = ChatHistoryRepository(mock_db_session)
    result = repository.read(mock_record.id)

    assert result is not None
    assert result.id == mock_record.id


# Test: Read a chat history record that does not exist
def test_read_chat_history_not_exists(mock_db_session):
    mock_db_session.query(ChatHistoryTable).filter(ChatHistoryTable.id == 999).first.return_value = None
    repository = ChatHistoryRepository(mock_db_session)
    result = repository.read(999)

    assert result is None
