"""Baseline existing CivicConnect database schema.

This migration represents the database schema that already existed
before the migration history was restored to this repository.

Revision ID: b03d35ce7368
Revises:
Create Date: 2026-10-05
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "b03d35ce7368"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Mark the existing database schema as the baseline."""
    pass


def downgrade() -> None:
    """No database objects are removed by the baseline migration."""
    pass