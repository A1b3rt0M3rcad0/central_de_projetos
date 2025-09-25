from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Users(BaseModel):
    cpf: str
    name: str
    email: str
    role: str
    created_at: str

class PaginationUsers(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    users: List[Users]

class FindAllUsersWithPaginationResponse(BaseResponse[PaginationUsers]):
    pass
