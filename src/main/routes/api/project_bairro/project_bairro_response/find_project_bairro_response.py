from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class FindProjectBairroContent(BaseModel):
    bairro_id:int
    project_id:int
    created_at:str

class FindProjectBairroResponse(BaseResponse[FindProjectBairroContent]):
    ...