#pylint:disable=all
"""empty message

Revision ID: fbcc8618f279
Revises: 841b92031e6b
Create Date: 2025-04-23 17:18:15.701299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbcc8618f279'
down_revision: Union[str, None] = '841b92031e6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'fiscal',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'project_fiscal',
        sa.Column('fiscal_id', sa.Integer, sa.ForeignKey('fiscal.id'), primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'bairro',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'project_bairro',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), primary_key=True),
        sa.Column('bairro_id', sa.Integer, sa.ForeignKey('bairro.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'empresa',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'project_empresa',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), primary_key=True),
        sa.Column('empresa_id', sa.Integer, sa.ForeignKey('empresa.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'types',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'project_type',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), primary_key=True),
        sa.Column('type_id', sa.Integer, sa.ForeignKey('types.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('project_fiscal')
    op.drop_table('project_type')
    op.drop_table('project_empresa')
    op.drop_table('project_bairro')

    op.drop_table('fiscal')
    op.drop_table('types')
    op.drop_table('empresa')
    op.drop_table('bairro')
