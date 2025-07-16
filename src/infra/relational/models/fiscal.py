from sqlalchemy import String, DateTime
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Fiscal(BaseModel):

    __tablename__ = 'fiscal'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100))
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    project_fiscals:Mapped[List["ProjectFiscal"]] = relationship("ProjectFiscal", back_populates='fiscal', lazy="selectin")