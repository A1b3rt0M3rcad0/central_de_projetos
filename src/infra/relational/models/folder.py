from sqlalchemy import String, DateTime
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.relational.models.project_folder import ProjectFolder

class Folder(BaseModel):

    __tablename__ = "folders"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    project_folders:Mapped[List["ProjectFolder"]] = relationship("ProjectFolder", back_populates="folder", lazy="selectin")