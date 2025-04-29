from sqlalchemy import DateTime, Column, Integer, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone

class ProjectEmpresa(BaseModel):

    __tablename__ = 'project_empresa'

    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresa.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)