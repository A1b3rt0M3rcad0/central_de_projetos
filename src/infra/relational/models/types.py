from sqlalchemy import String, DateTime, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Types(BaseModel):

    __tablename__ = 'types'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100), unique=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    project_types:Mapped[List["ProjectType"]] = relationship("ProjectType", back_populates='types')