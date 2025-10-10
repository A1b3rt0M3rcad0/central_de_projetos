from sqlalchemy import String, DateTime, LargeBinary
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class User(BaseModel):
    
    __tablename__ = 'user'

    cpf:Mapped[str] = mapped_column(String(15), primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=True)
    password:Mapped[bytes] = mapped_column(LargeBinary(255), nullable=False)
    salt:Mapped[bytes] = mapped_column(LargeBinary(255), nullable=False)
    role:Mapped[str] = mapped_column(String(50), nullable=False)
    email:Mapped[str] = mapped_column(String(50), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user_projects:Mapped[List["UserProject"]] = relationship("UserProject", back_populates='user')
    refresh_token:Mapped["RefreshToken"] = relationship("RefreshToken", back_populates='user')
    notifications:Mapped[List["Notification"]] = relationship("Notification", foreign_keys="Notification.recipient_cpf", back_populates='recipient')
    created_eaps:Mapped[List["EAP"]] = relationship("EAP", back_populates='creator')