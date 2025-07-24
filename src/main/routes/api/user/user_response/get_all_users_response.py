from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    cpf:str
    email:str
    role:str
    created_at:str

class GetAllUsersResponse(BaseResponse[List[User]]):
    ...