from typing import Dict, List, TypedDict
from src.domain.entities.types import TypesEntity

class ProjectTypesCountByBairro(TypedDict):
    types: List[TypesEntity]
    types_count_by_bairro: Dict[int, Dict[str, Dict[str, int]]]