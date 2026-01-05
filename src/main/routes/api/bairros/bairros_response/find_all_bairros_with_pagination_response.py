from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Bairros(BaseModel):
    id: int
    name: str
    created_at: str

class PaginationBairros(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    bairros: List[Bairros]

class FindAllBairrosWithPaginationResponse(BaseResponse[PaginationBairros]):
    pass
