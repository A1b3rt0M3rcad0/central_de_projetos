from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class ProjectType(BaseModel):
    project_id:int
    types_id:int
    created_at:str

class FindTypeFromProjectResponse(BaseResponse[List[ProjectType]]):
    ...