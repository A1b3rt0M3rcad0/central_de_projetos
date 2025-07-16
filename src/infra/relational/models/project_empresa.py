from sqlalchemy import DateTime, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProjectEmpresa(BaseModel):

    __tablename__ = 'project_empresa'

    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), primary_key=True)
    empresa_id:Mapped[int] = mapped_column(Integer, ForeignKey('empresa.id'), primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project:Mapped["Project"] = relationship("Project", back_populates="project_empresas")
    empresa:Mapped["Empresa"] = relationship("Empresa", back_populates="project_empresas")