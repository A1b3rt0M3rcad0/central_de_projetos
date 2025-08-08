from pydantic import BaseModel
from typing import Optional

class CreateWorkProjectMobileResponse(BaseModel):
    message: str
    work_project_id: int
    title: str
    photo_name: Optional[str] = None
    documents_count: int 