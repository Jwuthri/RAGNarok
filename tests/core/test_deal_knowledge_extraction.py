import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.core.deal_knowledge_extraction import DealKnowledgeExtraction
from src.schemas import DealKnowledgeExtractionSchema, ChatMessageSchema, PromptSchema
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly
from src.infrastructure.completion_parser import ListParser


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def inputs():
    return DealKnowledgeExtractionSchema(bot_id="test_bot", deal_id="test_deal", org_id="test_org")


@pytest.fixture
def deal_knowledge_extraction(db_session, inputs):
    return DealKnowledgeExtraction(db_session, inputs)


def test_initialization(deal_knowledge_extraction, db_session, inputs):
    assert deal_knowledge_extraction.db_session is db_session
    assert deal_knowledge_extraction.inputs is inputs


@patch("src.core.deal_knowledge_extraction.OpenaiChat")
def test_chat_completion(mock_openai_chat, deal_knowledge_extraction):
    mock_chat_instance = mock_openai_chat.return_value
    mock_chat_instance.predict.return_value = PromptSchema(
        prediction="What are the sales projections?",
        cost=0,
        latency=0,
        completion_tokens=0,
        prompt_tokens=0,
        llm_name="gpt4",
    )

    messages = [
        ChatMessageSchema(chat_id="msg1", message="message", role="assistant"),
        ChatMessageSchema(chat_id="msg2", message="message", role="user"),
    ]
    result = deal_knowledge_extraction.chat_completion(messages)
    assert isinstance(result, PromptSchema)
    assert result.prediction == "What are the sales projections?"
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())


def test_parse_completion(deal_knowledge_extraction):
    completion = "['company', 'sells', 'software']"
    deal_knowledge_extraction.parse_completion = Mock(return_value=ListParser.parse(text=completion))
    result = deal_knowledge_extraction.parse_completion(completion)
    assert result.parsed_completion == ["company", "sells", "software"]


def test_prediction_to_knowledge_graph(deal_knowledge_extraction, inputs):
    knowledge = {"subject": "company", "predicate": "sells", "object": "software", "timestamp": "2021-01-01"}
    result = deal_knowledge_extraction.prediction_to_knowledge_graph(knowledge)
    assert result.knowledge_text == "company sells software"
    assert result.meeting_timestamp == "2021-01-01"
    assert result.knowledge == knowledge


@patch("src.core.deal_knowledge_extraction.DealKnowledgeExtractionRepository")
def test_store_to_db_base_model(mock_repository, deal_knowledge_extraction, db_session):
    input_model = DealKnowledgeExtractionSchema(bot_id="bot_id", deal_id="deal_id", org_id="org_id")
    mock_repo_instance = mock_repository.return_value
    mock_repo_instance.create.return_value = input_model

    result = deal_knowledge_extraction.store_to_db_base_model([input_model])
    assert isinstance(result[0], DealKnowledgeExtractionSchema)
    mock_repository.assert_called_once_with(db_session)
    mock_repo_instance.create.assert_called_once_with(input_model)


@patch("src.core.deal_knowledge_extraction.CohereChat")
@patch("src.core.deal_knowledge_extraction.AnthropicChat")
@patch("src.core.deal_knowledge_extraction.OpenaiChat")
def test_chat_completion_with_exceptions(
    mock_openai_chat, mock_anthropic_chat, mock_cohere_chat, deal_knowledge_extraction
):
    mock_openai_chat.return_value.predict.side_effect = Exception("OpenAI service failure")
    mock_anthropic_chat.return_value.predict.side_effect = Exception("Anthropic service failure")
    expected_response = PromptSchema(
        prediction="Fallback success", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="gpt4"
    )
    mock_cohere_chat.return_value.predict.return_value = expected_response

    messages = [
        ChatMessageSchema(chat_id="msg1", message="message", role="assistant"),
        ChatMessageSchema(chat_id="msg2", message="message", role="user"),
    ]
    result = deal_knowledge_extraction.chat_completion(messages)
    assert result == expected_response
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())
    mock_anthropic_chat.assert_called_once_with(ChatAnthropicClaude3Haiku())
    mock_cohere_chat.assert_called_once_with(ChatCohereCommandLightNightly())
