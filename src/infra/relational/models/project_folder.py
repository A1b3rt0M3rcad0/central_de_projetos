from sqlalchemy import String, DateTime, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.relational.models.project import Project
    from src.infra.relational.models.folder import Folder

class ProjectFolder(BaseModel):

    __tablename__ = "project_folders"

    id:Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    folder_id:Mapped[str] = mapped_column(String(36), ForeignKey('folders.id'), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    project:Mapped["Project"] = relationship("Project", back_populates="project_folders")
    folder:Mapped["Folder"] = relationship("Folder", back_populates="project_folders")