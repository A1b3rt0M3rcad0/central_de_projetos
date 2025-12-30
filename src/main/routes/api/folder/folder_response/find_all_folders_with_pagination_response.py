from pydantic import BaseModel
from typing import List
from src.main.routes.api.__base_response.base_response import BaseResponse

class FolderContent(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

class PaginationContent(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    folders: List[FolderContent]

class FindAllFoldersWithPaginationResponse(BaseResponse[PaginationContent]):
    ...

