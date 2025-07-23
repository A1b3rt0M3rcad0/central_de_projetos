from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Status(BaseModel):
    id:int
    description:str
    created_at:str 

class GenericModel(BaseModel):
    id:int
    name:str
    created_at:str

class HistoryProject(BaseModel):
    id:int
    project_id:int
    description:str
    data_name:str
    updated_at:str

class User(BaseModel):
    cpf:str
    name:str

class Project(BaseModel):
    id:int
    name:str
    status:Status
    empresa:GenericModel
    fiscal:GenericModel
    types:GenericModel
    history_project:List[HistoryProject]
    andamento_do_projeto:str
    expected_completion_date:str
    end_date:str
    start_date:str
    verba_disponivel:float
    documents:List[str]
    user:User

class ProjectDetailResponse(BaseResponse[Project]):
    ...