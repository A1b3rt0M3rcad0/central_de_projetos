from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey

class RefreshToken(BaseModel):

    __tablename__ = "refresh_token"

    user_cpf = Column(String(15), ForeignKey('user.cpf'), primary_key=True, unique=True)
    token = Column(String(255), nullable=False)