from pydantic import BaseModel

class CreateWorkProjectWithFiscalDocumentFormat(BaseModel):
    project_id: int
    fiscal_id: int
    title: str
    description: str 