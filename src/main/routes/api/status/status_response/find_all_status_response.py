from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Status(BaseModel):
    id:int
    description:str
    created_at:str

class FindAllStatusResponse(BaseResponse[List[Status]]):
    ...