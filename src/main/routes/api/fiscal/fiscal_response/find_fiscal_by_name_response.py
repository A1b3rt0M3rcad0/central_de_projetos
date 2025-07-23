from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class FindFiscalByNameContent(BaseModel):
    id:int
    name:str
    created_at:str

class FindFiscalByNameResponse(BaseResponse[FindFiscalByNameContent]):
    ...