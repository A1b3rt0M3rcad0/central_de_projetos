from src.main.routes.api.__base_response.base_response import BaseResponse
from typing import List, Optional
from pydantic import BaseModel

class FindAllFiscalContent(BaseModel):
    id:int
    name:str
    email:Optional[str]
    phone:Optional[str]
    created_at:str

class FindAllFiscalReponse(BaseResponse[List[FindAllFiscalContent]]):
    ...