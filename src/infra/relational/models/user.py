from sqlalchemy import String, Column, DateTime, LargeBinary
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, backref
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.refresh_token import RefreshToken

class User(BaseModel):
    
    __tablename__ = 'user'

    name = Column(String(100), nullable=True)
    cpf = Column(String(15), primary_key=True)
    password = Column(LargeBinary(70), nullable=False)
    salt = Column(LargeBinary(100), nullable=False)
    role = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user_project = relationship(UserProject, backref=backref('user'))
    refresh_token = relationship(RefreshToken, backref=backref('user'))