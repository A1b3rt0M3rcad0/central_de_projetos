from sqlalchemy import Column, DateTime, ForeignKey
from src.infra.relational.config.base.base_model import BaseModel
from datetime import datetime, timezone

class UserProject(BaseModel):

    __tablename__ = 'user_project'

    user_cpf = Column(ForeignKey('user.cpf'), nullable=False, primary_key=True)
    project_id = Column(ForeignKey('project.id'), nullable=False, primary_key=True)
    assignment_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)