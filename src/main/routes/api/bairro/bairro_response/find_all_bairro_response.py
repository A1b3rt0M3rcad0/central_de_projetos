from pydantic import BaseModel
from typing import List
from src.main.routes.api.__base_response.base_response import BaseResponse

class BairroContent(BaseModel):
    id:int
    name:str
    created_at:str

class FindAllBairroResponse(BaseResponse[List[BairroContent]]):
    ...