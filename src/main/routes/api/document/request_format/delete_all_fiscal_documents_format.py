from pydantic import BaseModel

class DeleteAllFiscalDocumentsFormat(BaseModel):
    project_id: int
    fiscal_id: int 