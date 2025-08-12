#pylint:disable=all
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FiscalInfo(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class FiscalizacaoPorProjeto(BaseModel):
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    count: int

class UltimaFiscalizacao(BaseModel):
    id: int
    title: str
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    created_at: Optional[str] = None

class FiscalSummaryContent(BaseModel):
    fiscal: FiscalInfo
    total_projetos_vinculados: int
    total_fiscalizacoes: int
    fiscalizacoes_no_periodo: int
    last_activity_at: Optional[str] = None
    fiscalizacoes_por_projeto: List[FiscalizacaoPorProjeto]
    ultimas_fiscalizacoes: List[UltimaFiscalizacao]
    documentos_enviados: int

class GetFiscalSummaryResponse(BaseModel):
    message: str
    fiscal_id: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    content: FiscalSummaryContent 