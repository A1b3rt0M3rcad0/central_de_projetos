from pydantic import BaseModel
from typing import Optional, List, Any

class FiscalResponse(BaseModel):
    id: int
    name: str
    created_at: str

class ProjectResponse(BaseModel):
    id: int
    status_id: int
    name: str
    andamento_do_projeto: str
    verba_disponivel: str
    start_date: Optional[str] = None
    expected_completion_date: Optional[str] = None
    end_date: Optional[str] = None

class WorkProjectContentResponse(BaseModel):
    id: int
    project_id: int
    fiscal_id: int
    title: str
    description: str
    photo_name: str
    additional_documents: Optional[List[Any]] = None
    created_at: str
    updated_at: str
    fiscal: Optional[FiscalResponse] = None
    project: Optional[ProjectResponse] = None

class GetWorkProjectByFiscalMobileResponse(BaseModel):
    message: str
    content: WorkProjectContentResponse 