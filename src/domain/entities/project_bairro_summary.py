from typing import Dict, List, TypedDict
from src.domain.entities.bairro import BairroEntity

class ProjectBairroSummary(TypedDict):
    bairros: List[BairroEntity]
    projectBairro: Dict[str, int]
