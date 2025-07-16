from sqlalchemy import DateTime, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProjectBairro(BaseModel):

    __tablename__ = "project_bairro"

    bairro_id:Mapped[int] = mapped_column(Integer, ForeignKey('bairro.id'), primary_key=True)
    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    bairro:Mapped["Bairro"] = relationship("Bairro", back_populates="project_bairros")
    project:Mapped["Project"] = relationship("Project", back_populates="project_bairros")