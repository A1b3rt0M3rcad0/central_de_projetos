from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime, timezone
from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProjectType(BaseModel):

    __tablename__ = 'project_type'

    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), primary_key=True)
    type_id:Mapped[int] = mapped_column(Integer, ForeignKey('types.id'), primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    types:Mapped["Types"] = relationship("Types", back_populates="project_types")
    project:Mapped["Project"] = relationship("Project", back_populates="project_types")