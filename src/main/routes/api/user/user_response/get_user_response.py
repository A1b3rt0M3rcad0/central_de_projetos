from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class User(BaseModel):
    cpf:str
    email:str
    role:str
    created_at:str

class GetUserResponse(BaseResponse[User]):
    ...