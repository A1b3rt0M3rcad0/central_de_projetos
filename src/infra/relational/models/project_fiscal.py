from sqlalchemy import Integer, ForeignKey, DateTime, Column
from datetime import datetime, timezone
from src.infra.relational.config.base.base_model import BaseModel

class ProjectFiscal(BaseModel):

    __tablename__ = 'project_fiscal'

    fiscal_id = Column(Integer, ForeignKey('fiscal.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)