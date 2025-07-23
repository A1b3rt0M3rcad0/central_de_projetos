from src.main.routes.api.__base_response.base_response import BaseResponse
from typing import List, Optional
from pydantic import BaseModel

class ProjectDetails(BaseModel):
    id:int
    name:str
    bairro:Optional[str]
    empresa:Optional[str]
    fiscal:Optional[str]
    status:Optional[str]
    andamento_do_projeto:str
    user:Optional[str]
    expected_completion_date:Optional[str]
    start_date:Optional[str]
    end_date:Optional[str]
    verba_disponivel:float
    types:Optional[str]

class FindAllProjectWithBasicDetailsResponse(BaseResponse[List[ProjectDetails]]):
    ...