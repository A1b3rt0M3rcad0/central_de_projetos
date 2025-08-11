#pylint:disable=W0611
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectResponse(BaseModel):
    id: int
    status_id: int
    name: str
    andamento_do_projeto: str
    verba_disponivel: Optional[float]
    start_date: Optional[str]
    expected_completion_date: Optional[str]
    end_date: Optional[str]

class FiscalResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[str]

class WorkProjectResponse(BaseModel):
    id: int
    project_id: int
    fiscal_id: int
    title: str
    description: str
    photo_name: Optional[str]
    additional_documents: Optional[List[str]]
    created_at: Optional[str]
    updated_at: Optional[str]
    fiscal: Optional[FiscalResponse]
    project: Optional[ProjectResponse]

class GetLatestWorkProjectsByFiscalResponse(BaseModel):
    message: str
    total: int
    page: int
    page_size: int
    fiscal_id: int
    start_date: Optional[str]
    end_date: Optional[str]
    content: List[WorkProjectResponse] 