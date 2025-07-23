from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class ProjectContent(BaseModel):
    id:int
    name:str
    status_id:int
    verba_disponivel:float
    andamento_do_projeto:str
    start_date:str
    expected_completion_date:str
    end_date:str

class FindProjectResponse(BaseResponse[ProjectContent]):
    ...