import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from src.core.live_question_extraction import LiveQuestionExtraction
from src.schemas import LiveQuestionSchema, ChatMessageSchema, PromptSchema


def test_initialization():
    db_session = Mock(spec=Session)
    inputs = LiveQuestionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")
    extraction = LiveQuestionExtraction(db_session, inputs)
    assert extraction.db_session is db_session
    assert extraction.inputs is inputs


@patch("src.core.live_question_extraction.OpenaiChat")
@patch("src.core.live_question_extraction.ChatMessageRepository")
@patch("src.core.live_question_extraction.PromptRepository")
def test_predict(mock_prompt_repo, mock_chat_msg_repo, mock_openai_chat):
    db_session = Mock(spec=Session)
    inputs = LiveQuestionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")
    extraction = LiveQuestionExtraction(db_session, inputs)

    # Mock the methods called within predict
    extraction.fetch_history_messages = Mock()
    extraction.get_user_message = Mock()
    extraction.get_assistant_message = Mock()

    # Mock the return values
    history_message_mock = Mock(spec=ChatMessageSchema, chat_id="test_chat_id")
    extraction.fetch_history_messages.return_value = [history_message_mock]
    extraction.get_user_message.return_value = Mock(spec=ChatMessageSchema, chat_id="test_chat_id")
    mock_openai_chat_instance = mock_openai_chat.return_value
    mock_openai_chat_instance.predict.return_value = Mock(spec=PromptSchema, id="test_prompt_id")
    extraction.get_assistant_message.return_value = Mock(spec=ChatMessageSchema, chat_id="test_chat_id")

    extraction.predict()

    # Assertions to ensure the expected interactions
    assert extraction.fetch_history_messages.called
    assert extraction.get_user_message.called
    assert mock_openai_chat_instance.predict.called
    assert extraction.get_assistant_message.called
    mock_prompt_repo.assert_called_once()
    mock_chat_msg_repo.assert_called()
