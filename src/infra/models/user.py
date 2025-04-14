from sqlalchemy import String, Column, DateTime, LargeBinary
from src.infra.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, backref

class User(BaseModel):
    
    __tablename__ = 'user'

    cpf = Column(String(15), primary_key=True)
    password = Column(LargeBinary(70), nullable=False)
    salt = Column(LargeBinary(100), nullable=False)
    role = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime(timezone.utc))

    user_project = relationship('UserProject', backref=backref('user'))