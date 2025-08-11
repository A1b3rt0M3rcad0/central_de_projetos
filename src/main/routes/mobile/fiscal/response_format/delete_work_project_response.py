from pydantic import BaseModel

class DeleteWorkProjectMobileResponse(BaseModel):
    message: str
    work_project_id: int
    fiscal_id: int 