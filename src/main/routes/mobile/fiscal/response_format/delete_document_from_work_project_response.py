from pydantic import BaseModel

class DeleteDocumentFromWorkProjectMobileResponse(BaseModel):
    message: str
    work_project_id: int
    fiscal_id: int
    document_name: str 