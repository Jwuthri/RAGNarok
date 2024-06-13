"""Initial migration

Revision ID: 11f78cfc9735
Revises:
Create Date: 2024-06-13 01:02:35.333608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "11f78cfc9735"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "org",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("creator_type", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "prompt",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("prompt", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("llm_name", sa.String(), nullable=True),
        sa.Column("latency", sa.Float(), nullable=True),
        sa.Column("cost", sa.Float(), nullable=True),
        sa.Column("tool_call", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("prediction", sa.String(), nullable=True),
        sa.Column("prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("completion_tokens", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deal",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("owner", sa.String(), nullable=True),
        sa.Column("email_domain", sa.String(), nullable=True),
        sa.Column("contacts", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("creator_type", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("default", sa.Boolean(), nullable=True),
        sa.Column("creator_type", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("in_meeting", sa.Boolean(), nullable=True),
        sa.Column("meeting_id", sa.String(), nullable=True),
        sa.Column("meeting_url", sa.String(), nullable=True),
        sa.Column("meeting_platform", sa.String(), nullable=True),
        sa.Column(
            "meeting_metadata", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True
        ),
        sa.Column(
            "meeting_participants",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'"),
            nullable=True,
        ),
        sa.Column("join_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column(
            "status_changes", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True
        ),
        sa.Column(
            "participants", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=True
        ),
        sa.Column("recording", sa.String(), nullable=True),
        sa.Column("video_url", sa.String(), nullable=True),
        sa.Column("s3_video_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "discovery_question",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("question", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "followup_email_generation",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("generated_email", sa.String(), nullable=True),
        sa.Column("prompt_id", sa.String(), nullable=True),
        sa.Column("highlights", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'"), nullable=True),
        sa.Column("creator_type", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "index_data",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot_chat",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("to", sa.String(), nullable=True),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("sender", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot_participants",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("employee", sa.Boolean(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("modified_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot_status",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("code_status", sa.String(), nullable=True),
        sa.Column("sub_code", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bot_transcription",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("recording_id", sa.String(), nullable=True),
        sa.Column("start_time", sa.Float(), nullable=True),
        sa.Column("end_time", sa.Float(), nullable=True),
        sa.Column("speaker", sa.String(), nullable=True),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("is_final", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "chat",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("chat_type", sa.String(), nullable=True),
        sa.Column("thread_id", sa.String(), nullable=True),
        sa.Column("assistant_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deal_discovery_question",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("prompt_id", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("discovery_question_id", sa.String(), nullable=True),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("answer", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["discovery_question_id"],
            ["discovery_question.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deal_knowledge_extraction",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("prompt_id", sa.String(), nullable=True),
        sa.Column("meeting_timestamp", sa.Float(), nullable=True),
        sa.Column("knowledge", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("knowledge_text", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "meeting_question_extraction",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("question", sa.String(), nullable=True),
        sa.Column("prompt_id", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["bot.id"],
        ),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ask_about",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("chat_id", sa.String(), nullable=False),
        sa.Column("prompt_id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("org_name", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("creator_type", sa.String(), nullable=True),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("product_name", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("deal_name", sa.String(), nullable=True),
        sa.Column("answer", sa.String(), nullable=True),
        sa.Column("summary", sa.String(), nullable=True),
        sa.Column("follow_up", sa.String(), nullable=True),
        sa.Column("inscope", sa.Boolean(), nullable=True),
        sa.Column("intent", sa.String(), nullable=True),
        sa.Column("modality", sa.String(), nullable=True),
        sa.Column("qa_type", sa.String(), nullable=True),
        sa.Column("source_urns", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("video_urn", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("image_urn", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("roadmap", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("fuds", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("knowledge_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("answered_from_cache", sa.Boolean(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["deal_id"],
            ["deal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "chat_message",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("chat_id", sa.String(), nullable=False),
        sa.Column("prompt_id", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompt.id"],
        ),
        sa.PrimaryKeyConstraint("id", "chat_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("chat_message")
    op.drop_table("ask_about")
    op.drop_table("meeting_question_extraction")
    op.drop_table("deal_knowledge_extraction")
    op.drop_table("deal_discovery_question")
    op.drop_table("chat")
    op.drop_table("bot_transcription")
    op.drop_table("bot_status")
    op.drop_table("bot_participants")
    op.drop_table("bot_chat")
    op.drop_table("index_data")
    op.drop_table("followup_email_generation")
    op.drop_table("discovery_question")
    op.drop_table("bot")
    op.drop_table("user")
    op.drop_table("product")
    op.drop_table("deal")
    op.drop_table("prompt")
    op.drop_table("org")
    # ### end Alembic commands ###