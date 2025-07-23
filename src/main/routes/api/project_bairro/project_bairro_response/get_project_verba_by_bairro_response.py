from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List, Dict

class BairroContent(BaseModel):
    id:int
    name:str
    created_at:str

class GetProjectVerbaByBairroContent(BaseModel):
    verba:Dict[str, float]
    bairros:List[BairroContent]

class GetProjectVerbaByBairroResponse(BaseResponse[GetProjectVerbaByBairroContent]):
    ...