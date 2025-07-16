from sqlalchemy import String, DateTime
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy.orm import Mapped, mapped_column

class Empresa(BaseModel):

    __tablename__ = 'empresa'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100), unique=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    project_empresas:Mapped[List["ProjectEmpresa"]] = relationship("ProjectEmpresa", back_populates='empresa', lazy="selectin")