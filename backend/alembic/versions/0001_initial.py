"""schema initial

Revision ID: 0001
Revises:
Create Date: 2026-06-12
"""
from typing import Sequence, Union

from alembic import op

from app.core.database import Base
import app.models  # noqa: F401  (populates the metadata)

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the whole schema from the SQLAlchemy metadata.
    Base.metadata.create_all(op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(op.get_bind())
