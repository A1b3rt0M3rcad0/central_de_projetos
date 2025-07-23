from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class CountEmpresasContent(BaseModel):
    empresa_name:int

class CountEmpresasResponse(BaseResponse[CountEmpresasContent]):
    ...