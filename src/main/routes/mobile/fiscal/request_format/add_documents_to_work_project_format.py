from pydantic import BaseModel
from typing import List

class AddDocumentsToWorkProjectMobileFormat(BaseModel):
    work_project_id: int
    documents: List[dict]  # Lista de documentos com name, content_type, content 