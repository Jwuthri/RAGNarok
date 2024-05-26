"""remove chat_id from discovery

Revision ID: 1cbd5bf196f8
Revises: b67640ce6024
Create Date: 2024-05-25 21:45:57.618510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1cbd5bf196f8"
down_revision: Union[str, None] = "b67640ce6024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("deal_discovery_question", "chat_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("deal_discovery_question", sa.Column("chat_id", sa.String(), nullable=True))
    op.create_foreign_key(None, "chat", ["chat_id"], ["id"])
    # ### end Alembic commands ###
