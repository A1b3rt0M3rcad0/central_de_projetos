from sqlalchemy import String, Column, DateTime, LargeBinary
from src.infra.config.base.base_model import BaseModel
from datetime import datetime, timezone

class User(BaseModel):
    __tablename__ = 'user'

    cpf = Column(String(15), primary_key=True)
    password = Column(LargeBinary(70), nullable=False)
    role = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime(timezone.utc))

    def __repr__(self):
        return f"<User(cpf='{self.cpf}', email='{self.email}', role='{self.role}')>"