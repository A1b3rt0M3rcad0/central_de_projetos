from sqlalchemy import DateTime, ForeignKey, String, Integer
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserProject(BaseModel):

    __tablename__ = 'user_project'

    user_cpf:Mapped[str] = mapped_column(String(15), ForeignKey('user.cpf'), nullable=False, primary_key=True)
    project_id:Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False, primary_key=True)
    assignment_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user:Mapped["User"] = relationship("User", back_populates="user_projects")
    project:Mapped["Project"] = relationship("Project", back_populates="user_projects")
