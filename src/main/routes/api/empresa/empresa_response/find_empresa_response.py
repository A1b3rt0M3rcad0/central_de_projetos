from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class FindEmpresaContent(BaseModel):
    id:int
    name:str
    created_at:str

class FindEmpresaResponse(BaseResponse[FindEmpresaContent]):
    ...