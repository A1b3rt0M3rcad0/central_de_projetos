"""Dashboard Data Response Model"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class DashboardMetadata(BaseModel):
    """Metadados do dashboard"""
    modules_requested: List[str]
    excluded_status: List[int]
    total_modules: int


class DashboardDataResponse(BaseModel):
    """Response model para dados do dashboard"""
    message: str
    content: Dict[str, Any]
    metadata: DashboardMetadata
    new_access_token: Optional[str] = None

