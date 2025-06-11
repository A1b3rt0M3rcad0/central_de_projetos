#pylint:disable=all
"""add constraint in fiscal name unique

Revision ID: 530a2ad311a7
Revises: de24638c4d6b
Create Date: 2025-06-11 14:22:56.247826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '530a2ad311a7'
down_revision: Union[str, None] = 'de24638c4d6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uq_fiscal_name", table_name="fiscal", columns=["name"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_fiscal_name", table_name="fiscal", type_="unique")
