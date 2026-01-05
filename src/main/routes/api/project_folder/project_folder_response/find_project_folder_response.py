from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class FindProjectFolderContent(BaseModel):
    id: int
    folder_id: int
    project_id: int
    created_at: str
    updated_at: str

class FindProjectFolderResponse(BaseResponse[FindProjectFolderContent]):
    ...

