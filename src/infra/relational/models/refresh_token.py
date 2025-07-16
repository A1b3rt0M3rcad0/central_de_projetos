from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

class RefreshToken(BaseModel):

    __tablename__ = "refresh_token"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_cpf:Mapped[str] = mapped_column(String(15), ForeignKey('user.cpf'), unique=True)
    token:Mapped[str] = mapped_column(String(255), nullable=False)

    user:Mapped["User"] = relationship("User", back_populates='refresh_token')