"""create save chat table

Revision ID: 1d2781c2cc68
Revises: d7253f978256
Create Date: 2026-03-13 17:57:59.637418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d2781c2cc68'
down_revision: Union[str, Sequence[str], None] = 'd7253f978256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "chat_history",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("user_message", sa.Text(), nullable=False),
        sa.Column("detected_emotion", sa.String(), nullable=True),
        sa.Column("bot_response", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("chat_history")