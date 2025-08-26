from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Project(BaseModel):
    id:int
    status_id:int
    verba_disponivel:float
    andamento_do_projeto:str
    expected_completion_date:str
    start_date:str
    end_date:str

class PaginationProjects(BaseModel):
    page:int
    page_size:int
    total_items:int
    total_pages:int
    projects:List[Project]

class GetProjectsWithPaginationReponse(BaseResponse[PaginationProjects]):
    ...