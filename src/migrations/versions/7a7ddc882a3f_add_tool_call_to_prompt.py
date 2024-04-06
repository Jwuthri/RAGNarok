"""add tool call to prompt

Revision ID: 7a7ddc882a3f
Revises: 0a16cc7f7885
Create Date: 2024-04-04 01:26:06.507796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7a7ddc882a3f"
down_revision: Union[str, None] = "0a16cc7f7885"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("chat_history", sa.Column("chat_message_id", sa.String(), nullable=True))
    op.create_foreign_key(None, "chat_history", "chat_message", ["chat_message_id"], ["id"])
    op.drop_column("chat_history", "chat_message")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chat_history",
        sa.Column("chat_message", postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "chat_history", type_="foreignkey")
    op.drop_column("chat_history", "chat_message_id")
    # ### end Alembic commands ###