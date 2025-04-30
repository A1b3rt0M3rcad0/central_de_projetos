from sqlalchemy import Integer, ForeignKey, DateTime, Column
from datetime import datetime, timezone
from src.infra.relational.config.base.base_model import BaseModel

class ProjectType(BaseModel):

    __tablename__ = 'project_type'

    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)