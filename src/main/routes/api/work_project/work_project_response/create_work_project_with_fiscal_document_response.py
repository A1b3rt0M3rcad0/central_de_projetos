from src.main.routes.api.__base_response.base_response import BaseResponse
from pydantic import BaseModel

class WorkProjectContent(BaseModel):
    message: str
    title: str
    photo_name: str | None
    documents_count: int

class CreateWorkProjectWithFiscalDocumentResponse(BaseResponse[WorkProjectContent]):
    ... 