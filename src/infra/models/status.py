from sqlalchemy import String, Column, DateTime, Integer
from src.infra.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import backref, relationship


class Status(BaseModel):

    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime(timezone.utc))

    project = relationship("Project", backref=backref('status'))