from sqlalchemy import String, Column, DateTime, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import backref, relationship
from src.infra.relational.models.project import Project


class Status(BaseModel):

    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    project = relationship(Project, backref=backref('status'))