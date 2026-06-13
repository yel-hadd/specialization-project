"""add alerts.metric_value

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-13
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The measured value behind the alert (average, absence rate, or point drop),
    # kept separate from the threshold so the frontend can render the message in
    # any language.
    op.add_column("alerts", sa.Column("metric_value", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("alerts", "metric_value")
