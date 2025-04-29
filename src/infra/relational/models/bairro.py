from sqlalchemy import String, DateTime, Column, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from src.infra.relational.models.project_bairro import ProjectBairro
from sqlalchemy.orm import relationship, backref

class Bairro(BaseModel):

    __tablename__ = "bairro"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project_bairro = relationship(ProjectBairro, backref=backref('bairro'))