from pydantic import BaseModel

class DeleteDocumentFormat(BaseModel):
    project_id:int
    document_name:str