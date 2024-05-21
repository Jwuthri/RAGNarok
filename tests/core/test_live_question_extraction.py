import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.core.live_question_extraction import LiveQuestionExtraction
from src.schemas import LiveQuestionExtractionSchema, ChatMessageSchema, PromptSchema
from src.infrastructure.completion_parser import JsonParser
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def inputs():
    return LiveQuestionExtractionSchema(bot_id="test_bot_id", deal_id="test_deal_id", org_id="test_org_id")


@pytest.fixture
def live_question_extraction(db_session, inputs):
    with patch.object(LiveQuestionExtraction, "set_company_info", return_value=None):
        return LiveQuestionExtraction(db_session, inputs)


def test_initialization(live_question_extraction, db_session, inputs):
    assert live_question_extraction.db_session is db_session
    assert live_question_extraction.inputs is inputs


@patch("src.core.live_question_extraction.OpenaiChat")
def test_chat_completion(mock_openai_chat, live_question_extraction):
    mock_chat_instance = mock_openai_chat.return_value
    mock_chat_instance.predict.return_value = PromptSchema(
        prediction="Predicted answer",
        cost=0,
        latency=0,
        completion_tokens=0,
        prompt_tokens=0,
        llm_name="gpt3.5",
    )

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = live_question_extraction.chat_completion(messages)
    assert isinstance(result, PromptSchema)
    assert result.prediction == "Predicted answer"
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())


def test_parse_completion(live_question_extraction):
    completion = '{"answer": "yes", "confidence": "5"}'
    live_question_extraction.parse_completion = Mock(return_value=JsonParser.parse(text=completion))
    result = live_question_extraction.parse_completion(completion)
    assert result.parsed_completion == {"answer": "yes", "confidence": "5"}


def test_enrich_base_model(live_question_extraction, inputs):
    parsed_completion = Mock(parsed_completion={"answer": "yes", "confidence": 5})
    live_question_extraction.enrich_base_model(parsed_completion)
    assert live_question_extraction.inputs.question_extracted == "yes"
    assert live_question_extraction.inputs.confidence == 5


@patch("src.repositories.LiveQuestionExtractionRepository")
def test_store_to_db_base_model(mock_repository, live_question_extraction, db_session, inputs):
    mock_repo_instance = mock_repository.return_value
    mock_repo_instance.create.return_value = inputs

    result = live_question_extraction.store_to_db_base_model(inputs)
    assert result == inputs


@patch("src.core.live_question_extraction.CohereChat")
@patch("src.core.live_question_extraction.AnthropicChat")
@patch("src.core.live_question_extraction.OpenaiChat")
def test_chat_completion_with_exceptions(
    mock_openai_chat, mock_anthropic_chat, mock_cohere_chat, live_question_extraction
):
    mock_openai_chat.return_value.predict.side_effect = Exception("OpenAI service failure")
    mock_anthropic_chat.return_value.predict.side_effect = Exception("Anthropic service failure")
    expected_response = PromptSchema(
        prediction="Fallback successful", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="gpt3.5"
    )
    mock_cohere_chat.return_value.predict.return_value = expected_response

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = live_question_extraction.chat_completion(messages)
    assert result == expected_response
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())
    mock_anthropic_chat.assert_called_once_with(ChatAnthropicClaude3Haiku())
    mock_cohere_chat.assert_called_once_with(ChatCohereCommandLightNightly())
