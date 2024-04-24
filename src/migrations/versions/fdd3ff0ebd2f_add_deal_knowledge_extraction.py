"""add deal-knowledge-extraction

Revision ID: fdd3ff0ebd2f
Revises: c6eecaba160e
Create Date: 2024-04-16 00:02:26.037480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "fdd3ff0ebd2f"
down_revision: Union[str, None] = "c6eecaba160e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "deal_knowledge_extraction",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=True),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("deal_id", sa.String(), nullable=True),
        sa.Column("seconds_ago", sa.Integer(), nullable=True),
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("deal_knowledge_extraction")
    # ### end Alembic commands ###