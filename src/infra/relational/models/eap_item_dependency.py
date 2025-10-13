"""
Model para dependências entre itens da EAP
"""
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from src.infra.relational.config.base.base_model import BaseModel


class EAPItemDependency(BaseModel):
    """
    Modelo que representa uma dependência entre dois itens da EAP.
    
    Sistema flexível: qualquer item pode depender de qualquer outro item,
    desde que não crie ciclos ou dependências de si mesmo/descendentes.
    
    Tipos de dependência:
    - FS (Finish-to-Start): Predecessor termina → Sucessor inicia [PADRÃO]
    - SS (Start-to-Start): Predecessor inicia → Sucessor inicia
    - FF (Finish-to-Finish): Predecessor termina → Sucessor termina
    - SF (Start-to-Finish): Predecessor inicia → Sucessor termina [RARO]
    """
    
    __tablename__ = 'eap_item_dependency'
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    # Item que DEPENDE (sucessor)
    successor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('eap_items.id', ondelete='CASCADE'),
        nullable=False,
        comment='Item que depende (sucessor)'
    )
    
    # Item do qual DEPENDE (predecessor)
    predecessor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('eap_items.id', ondelete='CASCADE'),
        nullable=False,
        comment='Item do qual depende (predecessor)'
    )
    
    # Tipo de dependência (padrão: FS)
    dependency_type: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        default='FS',
        server_default='FS',
        comment='Tipo: FS, SS, FF, SF'
    )
    
    # Lag em dias (pode ser positivo ou negativo)
    lag_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default='0',
        comment='Atraso em dias (pode ser negativo)'
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
    
    # Relacionamentos
    successor: Mapped["EAPItem"] = relationship(
        "EAPItem",
        foreign_keys=[successor_id],
        back_populates="predecessor_dependencies"
    )
    
    predecessor: Mapped["EAPItem"] = relationship(
        "EAPItem",
        foreign_keys=[predecessor_id],
        back_populates="successor_dependencies"
    )
    
    def __repr__(self):
        return (
            f"<EAPItemDependency("
            f"id={self.id}, "
            f"successor={self.successor_id}, "
            f"predecessor={self.predecessor_id}, "
            f"type={self.dependency_type}"
            f")>"
        )

