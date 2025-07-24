from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import Dict, List

class Types(BaseModel):
    id:int
    name:int
    created_at:str

class GetProjectTypesCountByBairroContent(BaseModel):
    types:List[Types]
    types_count_by_bairro:Dict[int, Dict[str, Dict[str, int]]]

class GetProjectTypesCountByBairroResponse(BaseResponse[GetProjectTypesCountByBairroContent]):
    ...
