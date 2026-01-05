#pylint:disable=all
"""create_eap_tables

Revision ID: create_eap_tables
Revises: 
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_eap_tables'
down_revision = '4708abc097bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create eaps table
    op.create_table('eaps',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('is_template', sa.Boolean(), nullable=False),
        sa.Column('template_source_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.String(length=15), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['user.cpf'], ),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.ForeignKeyConstraint(['template_source_id'], ['eaps.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create eap_items table
    op.create_table('eap_items',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('eap_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('type', sa.Enum('fase', 'entrega', 'atividade', 'tarefa', name='eap_item_type'), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('responsible', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('budget', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('status', sa.Enum('nao_iniciado', 'em_andamento', 'concluido', 'pausado', 'cancelado', 'bloqueado', name='eap_item_status'), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['eap_id'], ['eaps.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['eap_items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better performance
    op.create_index('ix_eaps_project_id', 'eaps', ['project_id'])
    op.create_index('ix_eaps_is_template', 'eaps', ['is_template'])
    op.create_index('ix_eap_items_eap_id', 'eap_items', ['eap_id'])
    op.create_index('ix_eap_items_parent_id', 'eap_items', ['parent_id'])
    op.create_index('ix_eap_items_code', 'eap_items', ['eap_id', 'code'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_eap_items_code', table_name='eap_items')
    op.drop_index('ix_eap_items_parent_id', table_name='eap_items')
    op.drop_index('ix_eap_items_eap_id', table_name='eap_items')
    op.drop_index('ix_eaps_is_template', table_name='eaps')
    op.drop_index('ix_eaps_project_id', table_name='eaps')
    
    # Drop tables
    op.drop_table('eap_items')
    op.drop_table('eaps')