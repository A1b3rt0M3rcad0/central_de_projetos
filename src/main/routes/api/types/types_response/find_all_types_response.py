from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Types(BaseModel):
    id:int
    name:str
    created_at:str

class FindAllTypesResponse(BaseResponse[List[Types]]):
    ...