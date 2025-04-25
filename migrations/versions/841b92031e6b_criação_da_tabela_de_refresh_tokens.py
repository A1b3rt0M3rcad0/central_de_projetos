#pylint:disable=all
"""Criação da tabela de refresh tokens

Revision ID: 841b92031e6b
Revises: 51c48f55f776
Create Date: 2025-04-22 18:46:24.842144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '841b92031e6b'
down_revision: Union[str, None] = '51c48f55f776'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'refresh_token',
        sa.Column('user_cpf', sa.String(15), sa.ForeignKey('user.cpf'), unique=True),
        sa.Column('token', sa.String(255), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('refresh_token')
