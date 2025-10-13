from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship

from src.infra.relational.config.base.base_model import BaseModel


class EAP(BaseModel):
    """Modelo SQLAlchemy para EAP (Estrutura Analítica do Projeto)"""
    
    __tablename__ = "eaps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    is_template = Column(Boolean, default=False, nullable=False)
    template_source_id = Column(Integer, ForeignKey("eaps.id"), nullable=True)
    created_by = Column(String(15), ForeignKey("user.cpf"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    project = relationship("Project", back_populates="eap")
    template_source = relationship("EAP", remote_side=[id], back_populates="derived_eaps")
    derived_eaps = relationship("EAP", back_populates="template_source")
    creator = relationship("User", back_populates="created_eaps")
    items = relationship("EAPItem", back_populates="eap", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<EAP(id={self.id}, name='{self.name}', project_id={self.project_id}, is_template={self.is_template})>"


class EAPItem(BaseModel):
    """Modelo SQLAlchemy para Item da EAP"""
    
    __tablename__ = "eap_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    eap_id = Column(Integer, ForeignKey("eaps.id"), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum("fase", "entrega", "atividade", "tarefa", name="eap_item_type"), nullable=False)
    parent_id = Column(Integer, ForeignKey("eap_items.id"), nullable=True)
    responsible = Column(String(255), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    budget = Column(Numeric(15, 2), nullable=False)
    status = Column(Enum("nao_iniciado", "em_andamento", "concluido", "pausado", "cancelado", "bloqueado", name="eap_item_status"), nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    eap = relationship("EAP", back_populates="items")
    parent = relationship("EAPItem", remote_side=[id], back_populates="children")
    children = relationship("EAPItem", back_populates="parent", cascade="all, delete-orphan")
    
    # Relacionamentos de dependências
    # Este item DEPENDE de (predecessores)
    predecessor_dependencies = relationship(
        "EAPItemDependency",
        foreign_keys="[EAPItemDependency.successor_id]",
        back_populates="successor",
        cascade="all, delete-orphan"
    )
    
    # Outros itens DEPENDEM deste (sucessores)
    successor_dependencies = relationship(
        "EAPItemDependency",
        foreign_keys="[EAPItemDependency.predecessor_id]",
        back_populates="predecessor",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<EAPItem(id={self.id}, code='{self.code}', name='{self.name}', type='{self.type}', eap_id={self.eap_id})>"