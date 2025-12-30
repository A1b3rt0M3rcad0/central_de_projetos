from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class FolderContent(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

class FindAllFoldersFromProjectResponse(BaseResponse[List[FolderContent]]):
    ...

