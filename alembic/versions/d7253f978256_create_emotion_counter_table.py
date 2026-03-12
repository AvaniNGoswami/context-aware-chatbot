"""create emotion_counter table

Revision ID: d7253f978256
Revises: 838e37d2ba6c
Create Date: 2026-03-12 23:18:00.675713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7253f978256'
down_revision: Union[str, Sequence[str], None] = '838e37d2ba6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "emotion_counter",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("distress_count", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("user_id")
    )

def downgrade():
    op.drop_table("emotion_counter")