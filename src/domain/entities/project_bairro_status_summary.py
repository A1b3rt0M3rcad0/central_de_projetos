from typing import Dict, List, TypedDict
from src.domain.entities.bairro import BairroEntity

class ProjectBairroStatusSummary(TypedDict):
    bairros: List[BairroEntity]
    project_status_by_bairro: Dict[int, Dict[str, Dict[str, int]]]
