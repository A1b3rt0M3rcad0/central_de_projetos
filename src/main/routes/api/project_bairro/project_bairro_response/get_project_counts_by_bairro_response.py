from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List, Dict

class Bairro(BaseModel):
    id:str
    name:str
    created_at:str

class GetProjecCountsByBairroContent(BaseModel):
    bairros:List[Bairro]
    counts:Dict[str, int]

class GetProjectCountByBairroResponse(BaseResponse[GetProjecCountsByBairroContent]):
    ...