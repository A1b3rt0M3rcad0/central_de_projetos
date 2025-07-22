from pydantic import BaseModel
from src.main.routes.api.__base_response.base_response import BaseResponse

class FindBairroByNameResponseContent(BaseModel):
    id:int
    name:str
    created_at:str

class FindBairroByNameResponse(BaseResponse[FindBairroByNameResponseContent]):
    ...