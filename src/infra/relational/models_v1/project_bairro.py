from sqlalchemy import DateTime, Column, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone

class ProjectBairro(BaseModel):

    __tablename__ = "project_bairro"

    bairro_id = Column(Integer, ForeignKey('bairro.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))