from sqlalchemy import String, DateTime, Column, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone

class Fiscal(BaseModel):

    __tablename__ = 'fiscal'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))