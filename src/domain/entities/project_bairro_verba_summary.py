from typing import Dict, List, TypedDict
from src.domain.entities.bairro import BairroEntity

class ProjectBairroVerbaSummary(TypedDict):
    bairros: List[BairroEntity]
    project_verba_by_bairro: Dict[str, float]