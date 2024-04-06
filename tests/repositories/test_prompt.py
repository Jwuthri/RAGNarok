import pytest
from datetime import datetime
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from src.repositories.prompt import PromptRepository
from src.db.prompt import PromptTable
from src.schemas.prompt import PromptSchema


mock_data = {
    "cost": 10.5,
    "latency": 0.5,
    "llm_name": "example_llm",
    "prediction": "some_prediction",
    "prompt_tokens": 5,
    "tool_call": None,
    "completion_tokens": 10,
    "prompt": [{"message": "Hello", "role": "user"}],
    "meta": {"key": "value"},
    "created_at": datetime.now(),
}
mock_record = PromptSchema(**mock_data)


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mocked database session.
    """
    return create_autospec(Session, instance=True, spec_set=True)


def test_create_prompt(mock_db_session):
    """
    Test case for create method of PromptRepository.
    """
    db_record = PromptTable(
        id=mock_record.id,
        tool_call=mock_record.tool_call,
        prompt=mock_record.prompt,
        llm_name=mock_record.llm_name,
        latency=mock_record.latency,
        cost=mock_record.cost,
        prediction=mock_record.prediction,
        prompt_tokens=mock_record.prompt_tokens,
        completion_tokens=mock_record.completion_tokens,
        created_at=mock_record.created_at,
        meta=mock_record.meta,
    )

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.query.return_value.first.return_value = db_record

    repository = PromptRepository(mock_db_session)
    result = repository.create(mock_record)

    assert result == mock_record
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_read_prompt_exists(mock_db_session):
    """
    Test reading a prompt record that exists in the database.
    """
    mock_db_session.query(PromptTable).filter(PromptTable.id == mock_record.id).first.return_value = mock_record
    repository = PromptRepository(mock_db_session)
    result = repository.read(mock_record.id)
    assert result is not None
    assert result.id == mock_record.id
    mock_db_session.query().filter().first.assert_called_once()


def test_read_prompt_not_exists(mock_db_session):
    """
    Test reading a prompt record that does not exist in the database.
    """
    mock_db_session.query(PromptTable).filter(PromptTable.id == mock_record.id).first.return_value = None
    repository = PromptRepository(mock_db_session)
    result = repository.read(mock_record.id)
    assert result is None
    mock_db_session.query().filter().first.assert_called_once()


def test_update_prompt_exists(mock_db_session):
    """
    Test updating a prompt record that exists in the database.
    """
    updated_data = mock_data.copy()
    updated_data["latency"] = 0.25  # Change a field to simulate update
    updated_record = PromptSchema(**updated_data)

    db_record = PromptTable(**mock_data)
    mock_db_session.query(PromptTable).filter(PromptTable.id == mock_record.id).first.return_value = db_record

    repository = PromptRepository(mock_db_session)
    result = repository.update(mock_record.id, updated_record)

    assert result.latency == 0.25
    assert mock_db_session.commit.called


def test_delete_prompt_exists(mock_db_session):
    """
    Test deleting a prompt record that exists in the database.
    """
    # Mock the delete operation to simulate that one record was deleted
    mock_db_session.query(PromptTable).filter(PromptTable.id == mock_record.id).delete.return_value = 1

    repository = PromptRepository(mock_db_session)
    result = repository.delete(mock_record.id)

    assert result == 1  # One record should be reported as deleted
    assert mock_db_session.commit.called


def test_delete_prompt_not_exists(mock_db_session):
    """
    Test trying to delete a prompt record that does not exist.
    """
    # Mock the delete operation to simulate no records were deleted
    mock_db_session.query(PromptTable).filter(PromptTable.id == 999).delete.return_value = 0

    repository = PromptRepository(mock_db_session)
    result = repository.delete(999)

    assert result == 0  # No records should be reported as deleted
    assert mock_db_session.commit.called
