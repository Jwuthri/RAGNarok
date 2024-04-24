from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from src.core.live_question_extraction import LiveQuestionExtraction
from src.schemas import LiveQuestionExtractionSchema, ChatMessageSchema, PromptSchema


def test_initialization():
    db_session = Mock(spec=Session)
    inputs = LiveQuestionExtractionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")
    extraction = LiveQuestionExtraction(db_session, inputs)
    assert extraction.db_session is db_session
    assert extraction.inputs is inputs


@patch("src.core.live_question_extraction.OpenaiChat")
def test_predict(mock_openai_chat):
    db_session = Mock(spec=Session)
    inputs = LiveQuestionExtractionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")
    extraction = LiveQuestionExtraction(db_session, inputs)

    # Set up mocks for message lists and completion
    extraction.fetch_history_messages = Mock(
        return_value=[
            ChatMessageSchema(chat_id="test_chat_id1", role="assistant", message="What is AI?"),
        ]
    )
    extraction.chat_completion = Mock()
    mock_chat_completion_result = PromptSchema(
        id="test_prompt_id",
        role="assistant",
        prompt_tokens=0.0,
        completion_tokens=0.0,
        prediction="What is AI?",
        cost=0.0,
        latency=0.0,
        llm_name="openai",
    )
    extraction.chat_completion.return_value = mock_chat_completion_result
    mock_openai_chat_instance = mock_openai_chat.return_value
    mock_openai_chat_instance.predict.return_value = Mock(spec=PromptSchema, id="test_prompt_id")
    # Perform prediction
    result = extraction.predict()

    # Assertions to ensure the expected interactions and outcomes
    extraction.fetch_history_messages.assert_called_once()
    assert result.question_extracted == None, "The result should match the expected mock prompt schema."
