from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Empresas(BaseModel):
    id: int
    name: str
    created_at: str

class PaginationEmpresas(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    empresas: List[Empresas]

class FindAllEmpresasWithPaginationResponse(BaseResponse[PaginationEmpresas]):
    pass
