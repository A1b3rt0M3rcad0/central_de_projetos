from sqlalchemy import String, DateTime, Column, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone

class Empresa(BaseModel):

    __tablename__ = 'empresa'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))