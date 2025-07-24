from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class UserInfo(BaseModel):
    name:str
    role:str

class WhoAmIReponse(BaseResponse[UserInfo]):
    ...