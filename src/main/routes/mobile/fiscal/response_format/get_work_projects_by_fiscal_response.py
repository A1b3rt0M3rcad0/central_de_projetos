from pydantic import BaseModel
from typing import Optional, List

class FiscalResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    status_id: int
    name: Optional[str] = None
    andamento_do_projeto: Optional[str] = None
    verba_disponivel: Optional[float] = None
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
    additional_documents: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    fiscal: Optional[FiscalResponse] = None
    project: Optional[ProjectResponse] = None

class GetWorkProjectsByFiscalMobileResponse(BaseModel):
    message: str
    total: int
    page: int
    page_size: int
    fiscal_id: int
    content: List[WorkProjectContentResponse] 