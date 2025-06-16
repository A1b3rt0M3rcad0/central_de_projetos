from pydantic import BaseModel

class DeleteProjectFiscalFormat(BaseModel):
    project_id:int
    fiscal_id:int