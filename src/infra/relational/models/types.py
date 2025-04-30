from sqlalchemy import String, DateTime, Column, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from src.infra.relational.models.project_type import ProjectType
from sqlalchemy.orm import backref, relationship

class Types(BaseModel):

    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    project_types = relationship(ProjectType, backref=backref('types'))