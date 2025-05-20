from pydantic import BaseModel

class CreateProjectEmpresaFormat(BaseModel):
    project_id:int
    empresa_id:int