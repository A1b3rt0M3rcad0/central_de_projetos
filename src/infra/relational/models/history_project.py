from datetime import datetime, timezone
from sqlalchemy import String, Column, DateTime, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel


class HistoryProject(BaseModel):

    __tablename__ = 'history_project'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False)
    column_name = Column(String(30), nullable=False)
    description = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)