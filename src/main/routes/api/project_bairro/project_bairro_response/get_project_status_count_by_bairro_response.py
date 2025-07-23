from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List, Dict

class Bairro(BaseModel):
    id:int
    name:str
    created_at:str

class GetProjectStatusCountByBairroContent(BaseModel):
    bairros:List[Bairro]
    status:Dict[int, Dict[str, Dict[str, int]]]

class GetProjectStatusCountByBairroResponse(BaseResponse[GetProjectStatusCountByBairroContent]):
    ...