from pydantic import BaseModel
from src.main.routes.api.__base_response.base_response import BaseResponse

class FolderContent(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

class FindFolderByIdResponse(BaseResponse[FolderContent]):
    ...

