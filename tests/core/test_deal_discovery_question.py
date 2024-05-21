import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.core.deal_discovery_question import DealDiscoveryQuestion
from src.schemas import DealDiscoveryQuestionSchema, ChatMessageSchema, PromptSchema
from src.infrastructure.completion_parser import JsonParser, ParserType
from src.infrastructure.chat import OpenaiChat, AnthropicChat, CohereChat
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def inputs():
    return DealDiscoveryQuestionSchema(
        deal_id="test_deal_id", org_id="test_org_id", discovery_question_id="test_question_id"
    )


@pytest.fixture
def deal_discovery_question(db_session, inputs):
    with patch.object(DealDiscoveryQuestion, "set_company_info", return_value=None):
        return DealDiscoveryQuestion(db_session, inputs)


def test_initialization(deal_discovery_question, db_session, inputs):
    assert deal_discovery_question.db_session is db_session
    assert deal_discovery_question.inputs is inputs


@patch("src.core.deal_discovery_question.OpenaiChat")
def test_chat_completion(mock_openai_chat, deal_discovery_question):
    mock_chat_instance = mock_openai_chat.return_value
    mock_chat_instance.predict.return_value = PromptSchema(
        prediction="Generated answer",
        cost=0,
        latency=0,
        completion_tokens=0,
        prompt_tokens=0,
        llm_name="gpt3.5",
    )

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = deal_discovery_question.chat_completion(messages)
    assert isinstance(result, PromptSchema)
    assert result.prediction == "Generated answer"
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())


def test_parse_completion(deal_discovery_question):
    completion = '{"answer": "yes", "confidence": "5"}'
    deal_discovery_question.parse_completion = Mock(return_value=JsonParser.parse(text=completion))
    result = deal_discovery_question.parse_completion(completion)
    assert result.parsed_completion == {"answer": "yes", "confidence": "5"}


def test_enrich_base_model(deal_discovery_question, inputs):
    parsed_completion = Mock(parsed_completion={"answer": "yes"})
    enriched_model = deal_discovery_question.enrich_base_model(parsed_completion)
    assert enriched_model.answer == "yes"


@patch("src.core.deal_discovery_question.CohereChat")
@patch("src.core.deal_discovery_question.AnthropicChat")
@patch("src.core.deal_discovery_question.OpenaiChat")
def test_chat_completion_with_exceptions(
    mock_openai_chat, mock_anthropic_chat, mock_cohere_chat, deal_discovery_question
):
    mock_openai_chat.return_value.predict.side_effect = Exception("OpenAI service failure")
    mock_anthropic_chat.return_value.predict.side_effect = Exception("Anthropic service failure")
    expected_response = PromptSchema(
        prediction="Fallback successful", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="gpt3.5"
    )
    mock_cohere_chat.return_value.predict.return_value = expected_response

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = deal_discovery_question.chat_completion(messages)
    assert result == expected_response
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())
    mock_anthropic_chat.assert_called_once_with(ChatAnthropicClaude3Haiku())
    mock_cohere_chat.assert_called_once_with(ChatCohereCommandLightNightly())
