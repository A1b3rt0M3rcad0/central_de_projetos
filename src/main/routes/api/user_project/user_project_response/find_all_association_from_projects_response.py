from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Association(BaseModel):
    cpf:str
    project_id:int
    data_atribuicao:str


class FindAllAssocitationFromProjectsResponse(BaseResponse[List[Association]]):
    ...