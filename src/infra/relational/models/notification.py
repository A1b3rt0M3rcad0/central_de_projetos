from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy import Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime


class Notification(BaseModel):
    __tablename__ = "notifications"

    id = mapped_column(Integer, primary_key=True, index=True)
    recipient_cpf = mapped_column(String(15), ForeignKey("user.cpf"), nullable=False, index=True)
    notification_type = mapped_column(String(50), nullable=False, index=True)
    title = mapped_column(String(255), nullable=False)
    message = mapped_column(Text, nullable=False)
    is_read = mapped_column(Boolean, default=False, nullable=False, index=True)
    read_at = mapped_column(DateTime, nullable=True)
    related_entity_id = mapped_column(Integer, nullable=True, index=True)
    related_entity_type = mapped_column(String(50), nullable=True, index=True)
    sender_cpf = mapped_column(String(15), ForeignKey("user.cpf"), nullable=True, index=True)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, index=True)
    updated_at = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relacionamentos
    recipient = relationship("User", foreign_keys=[recipient_cpf], back_populates="notifications")
    sender = relationship("User", foreign_keys=[sender_cpf])
