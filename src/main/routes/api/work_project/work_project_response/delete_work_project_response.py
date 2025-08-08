from pydantic import BaseModel

class DeleteWorkProjectResponse(BaseModel):
    message: str
    work_project_id: int 