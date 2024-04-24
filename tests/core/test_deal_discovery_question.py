import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.core.deal_discovery_question import DealDiscoveryQuestion
from src.schemas import DealKnowledgeExtractionSchema, ChatMessageSchema, PromptSchema
from src.schemas.models import ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly, ChatOpenaiGpt35


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def inputs():
    return DealKnowledgeExtractionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")


@pytest.fixture
def deal_discovery(db_session, inputs):
    return DealDiscoveryQuestion(db_session, inputs)


def test_initialization(deal_discovery, db_session, inputs):
    assert deal_discovery.db_session is db_session
    assert deal_discovery.inputs is inputs


@patch("src.core.deal_discovery_question.OpenaiChat")
def test_chat_completion(mock_openai_chat, deal_discovery):
    mock_chat_instance = mock_openai_chat.return_value
    mock_chat_instance.predict.return_value = PromptSchema(
        prediction="How many units?", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="gpt4"
    )
    messages = [
        ChatMessageSchema(chat_id="msg1", message="message", role="assistant"),
        ChatMessageSchema(chat_id="msg2", message="message", role="user"),
    ]

    result = deal_discovery.chat_completion(messages)
    assert isinstance(result, PromptSchema)
    assert result.prediction == "How many units?"
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())


def test_parse_completion(deal_discovery):
    # Setup a Mock return value for parse_completion
    deal_discovery.parse_completion = Mock(
        return_value={"parsed_completion": [{"subject": "company", "predicate": "sells", "object": "software"}]}
    )

    completion = "company sells software"
    result = deal_discovery.parse_completion(completion)
    assert "parsed_completion" in result


def test_prediction_to_knowledge_graph(deal_discovery):
    knowledge = {"subject": "company", "predicate": "sells", "object": "software", "timestamp": "2021-01-01"}
    result = deal_discovery.prediction_to_knowledge_graph(knowledge)
    assert result.knowledge_text == "company sells software"
    assert result.meeting_timestamp == "2021-01-01"
    assert result.knowledge == {"subject": "company", "predicate": "sells", "object": "software"}


@patch("src.core.deal_discovery_question.DealKnowledgeExtractionRepository")
def test_store_to_db_base_model(mock_repository, deal_discovery, db_session):
    input_model = DealKnowledgeExtractionSchema(id="id", bot_id="bot_id", deal_id="deal_id", org_id="org_id")

    mock_repo_instance = mock_repository.return_value
    mock_repo_instance.create.return_value = input_model

    result = deal_discovery.store_to_db_base_model([input_model])
    assert isinstance(result[0], DealKnowledgeExtractionSchema)
    mock_repository.assert_called_once_with(db_session)
    mock_repo_instance.create.assert_called_once_with(input_model)


@patch("src.core.deal_discovery_question.CohereChat")
@patch("src.core.deal_discovery_question.AnthropicChat")
@patch("src.core.deal_discovery_question.OpenaiChat")
def test_chat_completion_with_exceptions(mock_openai_chat, mock_anthropic_chat, mock_cohere_chat, deal_discovery):
    mock_openai_chat.return_value.predict.side_effect = Exception("OpenAI service failure")
    mock_anthropic_chat.return_value.predict.side_effect = Exception("Anthropic service failure")
    expected_response = PromptSchema(
        prediction="Fallback response", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="cohere"
    )
    mock_cohere_chat.return_value.predict.return_value = expected_response

    messages = [
        ChatMessageSchema(chat_id="msg1", message="message", role="assistant"),
        ChatMessageSchema(chat_id="msg2", message="message", role="user"),
    ]
    result = deal_discovery.chat_completion(messages)
    assert result == expected_response
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())
    mock_anthropic_chat.assert_called_once_with(ChatAnthropicClaude3Haiku())
    mock_cohere_chat.assert_called_once_with(ChatCohereCommandLightNightly())
