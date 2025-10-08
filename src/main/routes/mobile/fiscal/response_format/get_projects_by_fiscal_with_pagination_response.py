from pydantic import BaseModel
from typing import List, Optional

class Project(BaseModel):
    id: int
    status_id: int
    status_name: Optional[str] = None
    verba_disponivel: Optional[float]
    andamento_do_projeto: Optional[str]
    start_date: Optional[str]
    expected_completion_date: Optional[str]
    end_date: Optional[str]
    name: Optional[str]
    bairro_name: Optional[str] = None
    empresa_name: Optional[str] = None
    work_project_count: Optional[int] = None
    last_fiscalizacao_date: Optional[str] = None

class GetProjectsByFiscalWithPaginationMobileResponse(BaseModel):
    message: str
    page: int
    page_size: int
    total_items: int
    total_pages: int
    content: List[Project] 