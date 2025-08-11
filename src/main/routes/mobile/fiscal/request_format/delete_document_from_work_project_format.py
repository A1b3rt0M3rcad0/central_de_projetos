from pydantic import BaseModel, Field

class DeleteDocumentFromWorkProjectFormat(BaseModel):
    work_project_id: int = Field(..., description="ID do work project")
    document_name: str = Field(..., description="Nome do documento a ser deletado") 