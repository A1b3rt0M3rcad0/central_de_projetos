#pylint:disable=all
"""empty message

Revision ID: 51c48f55f776
Revises: 
Create Date: 2025-04-11 13:15:09.398333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51c48f55f776'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('cpf', sa.String(15), primary_key=True),
        sa.Column('password', sa.LargeBinary(70), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )
    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )
    op.create_table(
        'project',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id'), nullable=False),
        sa.Column('verba_disponivel', sa.Float, nullable=True),
        sa.Column('andamento_do_projeto', sa.String(255), nullable=True),
        sa.Column('start_date', sa.DateTime, nullable=True),
        sa.Column('expected_completion_date', sa.DateTime, nullable=True),
        sa.Column('end_date', sa.DateTime, nullable=True)
    )
    op.create_table(
        'history_project',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), nullable=False),
        sa.Column('data_name', sa.String(30), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )
    op.create_table(
        'user_project',
        sa.Column('user_cpf', sa.String(15), sa.ForeignKey('users.cpf'), nullable=False, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), nullable=False, primary_key=True),
        sa.Column('assignment_date', sa.DateTime,)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    op.drop_table('status')
    op.drop_table('project')
    op.drop_table('history_project')
    op.drop_table('user_project')
