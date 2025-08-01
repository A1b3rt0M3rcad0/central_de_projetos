from pydantic import BaseModel
from datetime import datetime
from src.domain.entities.fiscal import FiscalEntity
from src.domain.entities.project import ProjectEntity

class WorkProject(BaseModel):
    id: int
    project_id: int
    fiscal_id: int
    title: str
    description: str
    photo_name: str
    created_at: datetime
    updated_at: datetime
    fiscal: FiscalEntity
    project: ProjectEntity

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"<WorkProject(id={self.id}, project_id={self.project_id}, fiscal_id={self.fiscal_id}, title={self.title}, description={self.description}, photo_name={self.photo_name})>"