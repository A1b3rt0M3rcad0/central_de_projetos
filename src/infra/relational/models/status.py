from sqlalchemy import String, DateTime, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List


class Status(BaseModel):

    __tablename__ = 'status'
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description:Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    projects:Mapped[List["Project"]] = relationship("Project", back_populates='status', lazy="selectin")