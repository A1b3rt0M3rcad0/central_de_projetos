#pylint:disable=all
"""create_system_config_table

Revision ID: d1ee6b283dd7
Revises: 2c5c55cd68a7
Create Date: 2025-10-07 08:26:47.333256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1ee6b283dd7'
down_revision: Union[str, None] = '2c5c55cd68a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'system_config',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('config_key', sa.String(100), nullable=False, unique=True, comment='Chave da configuração'),
        sa.Column('config_value', sa.Text(), nullable=True, comment='Valor da configuração (JSON ou texto)'),
        sa.Column('description', sa.String(255), nullable=True, comment='Descrição da configuração'),
        sa.Column('config_type', sa.String(50), nullable=False, default='string', comment='Tipo: string, json, list, boolean, number'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='Se a configuração está ativa'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )
    
    # Inserir configurações padrão
    op.execute("""
        INSERT INTO system_config (config_key, config_value, description, config_type, is_active)
        VALUES 
        ('dashboard.excluded_status', '[]', 'Lista de IDs de status excluídos do dashboard', 'json', TRUE),
        ('dashboard.cache_ttl', '300', 'Tempo de cache do dashboard em segundos (5 minutos)', 'number', TRUE),
        ('dashboard.refresh_interval', '60000', 'Intervalo de atualização automática em ms (1 minuto)', 'number', TRUE),
        ('dashboard.show_inactive_projects', 'false', 'Mostrar projetos inativos no dashboard', 'boolean', FALSE),
        ('dashboard.max_top_items', '10', 'Número máximo de itens nas tabelas de top performers', 'number', TRUE)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('system_config')
