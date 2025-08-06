from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel
from typing import List

class AddDocumentsToWorkProjectContent(BaseModel):
    message: str
    documents_added: List[str]

class AddDocumentsToWorkProjectResponse(BaseResponse[AddDocumentsToWorkProjectContent]):
    ... 