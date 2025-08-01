from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime


class WorkProject(BaseModel):
    __tablename__ = "work_projects"

    id = mapped_column(Integer, primary_key=True, index=True)
    project_id = mapped_column(Integer, ForeignKey("project.id"))
    fiscal_id = mapped_column(Integer, ForeignKey("fiscal.id"))
    title = mapped_column(String(255), index=True)
    description = mapped_column(String(500), index=True)
    photo_name = mapped_column(String(255), index=True)
    created_at = mapped_column(DateTime, default=datetime.now)
    updated_at = mapped_column(DateTime, default=datetime.now)

    project = relationship("Project", back_populates="work_projects")
    fiscal = relationship("Fiscal", back_populates="work_projects")
    