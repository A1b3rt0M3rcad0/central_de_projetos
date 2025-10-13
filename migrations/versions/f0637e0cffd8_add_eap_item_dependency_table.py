#pylint:disable=all
"""add eap_item_dependency table

Revision ID: f0637e0cffd8
Revises: create_eap_tables
Create Date: 2025-10-12 20:26:35.837702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f0637e0cffd8'
down_revision: Union[str, None] = 'create_eap_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Criar tabela de dependências entre itens da EAP
    op.create_table(
        'eap_item_dependency',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('successor_id', sa.Integer(), nullable=False, comment='Item que depende (sucessor)'),
        sa.Column('predecessor_id', sa.Integer(), nullable=False, comment='Item do qual depende (predecessor)'),
        sa.Column('dependency_type', sa.String(length=5), server_default='FS', nullable=False, comment='Tipo: FS, SS, FF, SF'),
        sa.Column('lag_days', sa.Integer(), server_default='0', nullable=False, comment='Atraso em dias (pode ser negativo)'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['predecessor_id'], ['eap_items.id'], name='fk_dependency_predecessor', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['successor_id'], ['eap_items.id'], name='fk_dependency_successor', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criar índices para performance
    op.create_index('ix_dependency_successor', 'eap_item_dependency', ['successor_id'])
    op.create_index('ix_dependency_predecessor', 'eap_item_dependency', ['predecessor_id'])
    op.create_index('ix_dependency_type', 'eap_item_dependency', ['dependency_type'])
    
    # Índice único para evitar dependências duplicadas
    op.create_index('uq_dependency_pair', 'eap_item_dependency', ['successor_id', 'predecessor_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Remover índices
    op.drop_index('uq_dependency_pair', table_name='eap_item_dependency')
    op.drop_index('ix_dependency_type', table_name='eap_item_dependency')
    op.drop_index('ix_dependency_predecessor', table_name='eap_item_dependency')
    op.drop_index('ix_dependency_successor', table_name='eap_item_dependency')
    
    # Remover tabela
    op.drop_table('eap_item_dependency')
