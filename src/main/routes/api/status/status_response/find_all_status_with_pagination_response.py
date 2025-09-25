from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class Status(BaseModel):
    id: int
    description: str
    created_at: str

class PaginationStatus(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    status: List[Status]

class FindAllStatusWithPaginationResponse(BaseResponse[PaginationStatus]):
    pass
