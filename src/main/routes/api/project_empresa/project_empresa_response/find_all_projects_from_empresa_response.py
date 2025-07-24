from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class ProjectEmpresa(BaseModel):
    project_id:int
    empresa_id:int
    created_at:str

class FindAllProjectsFromEmpresaResponse(BaseResponse[List[ProjectEmpresa]]):
    ...