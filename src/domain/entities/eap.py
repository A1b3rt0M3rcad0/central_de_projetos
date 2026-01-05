from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from src.domain.value_objects.eap_code import EAPCode
from src.domain.value_objects.eap_type import EAPType
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue


@dataclass
class EAPItemEntity:
    """Entidade que representa um item da EAP (Estrutura Analítica do Projeto)"""
    
    id: Optional[int]
    eap_id: int
    code: EAPCode
    name: str
    description: str
    type: EAPType
    parent_id: Optional[int]
    responsible: str
    start_date: datetime
    end_date: datetime
    budget: MonetaryValue
    status: EAPStatus
    progress: int
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validações pós-inicialização"""
        if self.progress < 0 or self.progress > 100:
            raise ValueError("Progresso deve estar entre 0 e 100")
        
        if self.start_date > self.end_date:
            raise ValueError("Data de início não pode ser posterior à data de fim")
        
        if not self.name.strip():
            raise ValueError("Nome do item não pode estar vazio")
        
        if not self.description.strip():
            raise ValueError("Descrição do item não pode estar vazia")
        
        if not self.responsible.strip():
            raise ValueError("Responsável não pode estar vazio")


@dataclass
class EAPEntity:
    """Entidade que representa uma EAP (Estrutura Analítica do Projeto)"""
    
    id: Optional[int]
    name: str
    description: str
    project_id: int
    is_template: bool
    template_source_id: Optional[int]
    created_by: int
    created_at: datetime
    updated_at: datetime
    items: List[EAPItemEntity]
    
    def __post_init__(self):
        """Validações pós-inicialização"""
        if not self.name.strip():
            raise ValueError("Nome da EAP não pode estar vazio")
        
        if not self.description.strip():
            raise ValueError("Descrição da EAP não pode estar vazia")
        
        if self.is_template and self.project_id is not None:
            raise ValueError("EAP template não pode estar vinculada a um projeto específico")
        
        if not self.is_template and self.project_id is None:
            raise ValueError("EAP de projeto deve estar vinculada a um projeto")
    
    def get_total_budget(self) -> MonetaryValue:
        """Calcula o orçamento total da EAP"""
        total = sum(item.budget.value for item in self.items)
        return MonetaryValue(total)
    
    def get_progress_percentage(self) -> int:
        """Calcula o percentual de progresso geral da EAP"""
        if not self.items:
            return 0
        
        total_progress = sum(item.progress for item in self.items)
        return round(total_progress / len(self.items))
    
    def get_items_by_type(self, eap_type: EAPType) -> List[EAPItemEntity]:
        """Retorna todos os itens de um tipo específico"""
        return [item for item in self.items if item.type == eap_type]
    
    def get_items_by_status(self, eap_status: EAPStatus) -> List[EAPItemEntity]:
        """Retorna todos os itens com um status específico"""
        return [item for item in self.items if item.status == eap_status]
    
    def get_root_items(self) -> List[EAPItemEntity]:
        """Retorna todos os itens raiz (sem pai)"""
        return [item for item in self.items if item.parent_id is None]
    
    def get_children_items(self, parent_id: int) -> List[EAPItemEntity]:
        """Retorna todos os itens filhos de um item específico"""
        return [item for item in self.items if item.parent_id == parent_id]
    
    def validate_hierarchy(self) -> bool:
        """Valida se a hierarquia da EAP está correta"""
        # Verifica se não há ciclos na hierarquia
        visited = set()
        
        def has_cycle(item_id: int, path: set) -> bool:
            if item_id in path:
                return True
            if item_id in visited:
                return False
            
            visited.add(item_id)
            path.add(item_id)
            
            for item in self.items:
                if item.parent_id == item_id:
                    if has_cycle(item.id, path.copy()):
                        return True
            
            return False
        
        for item in self.items:
            if item.id not in visited:
                if has_cycle(item.id, set()):
                    return False
        
        return True
