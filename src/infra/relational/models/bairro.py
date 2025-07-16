from sqlalchemy import String, DateTime, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Bairro(BaseModel):

    __tablename__ = "bairro"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(100), unique=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project_bairros:Mapped[List["ProjectBairro"]] = relationship("ProjectBairro", back_populates="bairro", lazy="selectin")