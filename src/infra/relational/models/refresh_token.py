from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Integer

class RefreshToken(BaseModel):

    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_cpf = Column(String(15), ForeignKey('user.cpf'), unique=True)
    token = Column(String(255), nullable=False)