from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Project(BaseModel):
    id:int
    status_id:int
    name:str
    verba_disponivel:float
    andamento_do_projeto:str
    start_date:str
    expected_completion_date:str
    end_date:str

class FindProjectbyStatusReponse(BaseResponse[List[Project]]):
    ...