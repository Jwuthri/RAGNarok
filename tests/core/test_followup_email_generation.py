import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from src.core.followup_email_generation import FollowUpEmailGeneration
from src.schemas import FollowUpEmailGenerationSchema, ChatMessageSchema, PromptSchema
from src.infrastructure.completion_parser import StringParser
from src.schemas.models import ChatOpenaiGpt35, ChatAnthropicClaude3Haiku, ChatCohereCommandLightNightly


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def inputs():
    return FollowUpEmailGenerationSchema(
        org_id="test_org_id", user_id="test_user_id", creator_type="simulation", highlights=[]
    )


@pytest.fixture
def followup_email_generation(db_session, inputs):
    with patch.object(FollowUpEmailGeneration, "set_company_info", return_value=None):
        return FollowUpEmailGeneration(db_session, inputs)


def test_initialization(followup_email_generation, db_session, inputs):
    assert followup_email_generation.db_session is db_session
    assert followup_email_generation.inputs is inputs


@patch("src.core.followup_email_generation.OpenaiChat")
def test_chat_completion(mock_openai_chat, followup_email_generation):
    mock_chat_instance = mock_openai_chat.return_value
    mock_chat_instance.predict.return_value = PromptSchema(
        prediction="Here's your follow-up email content",
        cost=0,
        latency=0,
        completion_tokens=0,
        prompt_tokens=0,
        llm_name="gpt4",
    )

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = followup_email_generation.chat_completion(messages)
    assert isinstance(result, PromptSchema)
    assert result.prediction == "Here's your follow-up email content"
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())


def test_parse_completion(followup_email_generation):
    completion = "This is a generated follow-up email content"
    followup_email_generation.parse_completion = Mock(return_value=StringParser.parse(text=completion))
    result = followup_email_generation.parse_completion(completion)
    assert result.parsed_completion == completion


def test_enrich_base_model(followup_email_generation, inputs):
    parsed_completion = Mock(parsed_completion="Generated email content")
    enriched_model = followup_email_generation.enrich_base_model(parsed_completion)
    assert enriched_model.generated_email == "Generated email content"


@patch("src.core.followup_email_generation.FollowUpEmailGenerationRepository")
def test_store_to_db_base_model(mock_repository, followup_email_generation, db_session):
    input_model = FollowUpEmailGenerationSchema(org_id="org_id", user_id="user_id")
    mock_repo_instance = mock_repository.return_value
    mock_repo_instance.create.return_value = input_model

    result = followup_email_generation.store_to_db_base_model(input_model)
    assert result == input_model
    mock_repository.assert_called_once_with(db_session)
    mock_repo_instance.create.assert_called_once_with(input_model)


@patch("src.core.followup_email_generation.CohereChat")
@patch("src.core.followup_email_generation.AnthropicChat")
@patch("src.core.followup_email_generation.OpenaiChat")
def test_chat_completion_with_exceptions(
    mock_openai_chat, mock_anthropic_chat, mock_cohere_chat, followup_email_generation
):
    mock_openai_chat.return_value.predict.side_effect = Exception("OpenAI service failure")
    mock_anthropic_chat.return_value.predict.side_effect = Exception("Anthropic service failure")
    expected_response = PromptSchema(
        prediction="Fallback successful", cost=0, latency=0, completion_tokens=0, prompt_tokens=0, llm_name="gpt4"
    )
    mock_cohere_chat.return_value.predict.return_value = expected_response

    messages = [ChatMessageSchema(chat_id="msg1", message="Hello", role="user")]
    result = followup_email_generation.chat_completion(messages)
    assert result == expected_response
    mock_openai_chat.assert_called_once_with(ChatOpenaiGpt35())
    mock_anthropic_chat.assert_called_once_with(ChatAnthropicClaude3Haiku())
    mock_cohere_chat.assert_called_once_with(ChatCohereCommandLightNightly())
