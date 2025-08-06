from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class WorkProjectEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    id: int
    project_id: int
    fiscal_id: int
    title: str
    description: str
    photo_name: str
    additional_documents: Optional[list] = None  # JSON array of additional document names
    created_at: datetime
    updated_at: datetime
    fiscal: Optional[Any] = None
    project: Optional[Any] = None

    def __repr__(self):
        return f"<WorkProject(id={self.id}, project_id={self.project_id}, fiscal_id={self.fiscal_id}, title={self.title}, description={self.description}, photo_name={self.photo_name})>"