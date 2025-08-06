from pydantic import BaseModel
from typing import List

class AddDocumentsToWorkProjectMobileContent(BaseModel):
    message: str
    documents_added: List[str]

class AddDocumentsToWorkProjectMobileResponse(BaseModel):
    message: str
    documents_added: List[str] 