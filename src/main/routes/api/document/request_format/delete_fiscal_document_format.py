from pydantic import BaseModel

class DeleteFiscalDocumentFormat(BaseModel):
    project_id: int
    fiscal_id: int
    document_name: str 