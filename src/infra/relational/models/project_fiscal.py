from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProjectFiscal(BaseModel):

    __tablename__ = 'project_fiscal'

    fiscal_id:Mapped[int] = mapped_column(Integer, ForeignKey('fiscal.id'), primary_key=True)
    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    fiscal:Mapped["Fiscal"] = relationship("Fiscal", back_populates="project_fiscals")
    project:Mapped["Project"] = relationship("Project", back_populates="project_fiscals")