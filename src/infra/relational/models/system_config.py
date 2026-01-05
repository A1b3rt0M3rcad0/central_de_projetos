from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime


class SystemConfig(BaseModel):
    """Tabela de configurações do sistema"""
    __tablename__ = 'system_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), nullable=False, unique=True, comment='Chave da configuração')
    config_value = Column(Text, nullable=True, comment='Valor da configuração (JSON ou texto)')
    description = Column(String(255), nullable=True, comment='Descrição da configuração')
    config_type = Column(String(50), nullable=False, default='string', comment='Tipo: string, json, list, boolean, number')
    is_active = Column(Boolean, nullable=False, default=True, comment='Se a configuração está ativa')
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<SystemConfig(key='{self.config_key}', value='{self.config_value}')>"

