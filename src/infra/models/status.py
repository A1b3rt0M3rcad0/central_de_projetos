from sqlalchemy import String, Column, DateTime, Integer
from src.infra.config.base.base_model import BaseModel
from datetime import datetime, timezone


class Status(BaseModel):

    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime(timezone.utc))


    def __repr__(self) -> str:
        return f"<Status(id='{self.id}', description='{self.description}', created_at='{self.created_at}')>"