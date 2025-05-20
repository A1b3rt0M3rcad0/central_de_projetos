from pydantic import BaseModel

class DeleteProjectEmpresaFormat(BaseModel):
    project_id:int
    empresa_id:int