from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Fiscais(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    created_at: str

class PaginationFiscais(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    fiscais: List[Fiscais]

class FindAllFiscaisWithPaginationResponse(BaseResponse[PaginationFiscais]):
    pass
