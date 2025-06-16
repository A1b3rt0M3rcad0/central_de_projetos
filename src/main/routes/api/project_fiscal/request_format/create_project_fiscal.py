from pydantic import BaseModel

class CreateProjectFiscalFormat(BaseModel):
    project_id:int
    fiscal_id:int