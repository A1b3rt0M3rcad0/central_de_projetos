from src.main.routes.api.__base_response.base_response import BaseResponse
from typing import List
from pydantic import BaseModel

class FindAllFiscalContent(BaseModel):
    id:int
    name:str
    created_at:str

class FindAllFiscalReponse(BaseResponse[List[FindAllFiscalContent]]):
    ...