#pylint:disable=all
"""add_is_active_to_fiscal

Revision ID: 4708abc097bb
Revises: d1ee6b283dd7
Create Date: 2025-10-09 15:13:20.748275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4708abc097bb'
down_revision: Union[str, None] = 'd1ee6b283dd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Verifica se a coluna já existe antes de adicionar
    from sqlalchemy import inspect
    from sqlalchemy.engine import reflection
    
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('fiscal')]
    
    if 'is_active' not in columns:
        op.add_column('fiscal', sa.Column('is_active', sa.Integer(), nullable=True, server_default='1'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('fiscal', 'is_active')
