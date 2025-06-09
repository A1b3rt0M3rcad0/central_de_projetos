#pylint:disable=all
"""name colmun for user

Revision ID: de24638c4d6b
Revises: fbcc8618f279
Create Date: 2025-06-09 13:53:53.997183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de24638c4d6b'
down_revision: Union[str, None] = 'fbcc8618f279'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('name', sa.String(100), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'name')
    pass
