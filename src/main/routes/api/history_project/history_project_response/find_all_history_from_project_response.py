from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class HistoryContent(BaseModel):
    id:int
    project_id:int
    data_name:str
    description:str
    updated_at:str

class FindAllHistoryFromProjectReponse(BaseResponse[List[HistoryContent]]):
    ...