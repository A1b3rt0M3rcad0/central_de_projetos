from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HistoryProject(BaseModel):

    __tablename__ = 'history_project'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    data_name:Mapped[str] = mapped_column(String(30), nullable=False)
    description:Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project:Mapped["Project"] = relationship("Project", back_populates="history_projects")