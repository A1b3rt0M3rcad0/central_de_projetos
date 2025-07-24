from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class Status(BaseModel):
    id:int
    description:str
    created_at:str

class FindStatusReponse(BaseResponse[Status]):
    ...