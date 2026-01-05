"""
Entity para dependência entre itens da EAP
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from src.domain.value_objects.dependency_type import DependencyType


@dataclass
class EAPDependencyEntity:
    """
    Entidade que representa uma dependência entre dois itens da EAP.
    
    Representa a relação: "Item B depende do Item A"
    - Predecessor (A): Item que deve ser concluído primeiro
    - Successor (B): Item que depende do predecessor
    """
    
    id: Optional[int]
    successor_id: int
    predecessor_id: int
    dependency_type: DependencyType
    lag_days: int
    created_at: datetime
    updated_at: datetime
    
    # Informações extras para facilitar uso (não salvas no banco)
    successor_name: Optional[str] = None
    successor_code: Optional[str] = None
    predecessor_name: Optional[str] = None
    predecessor_code: Optional[str] = None
    
    def __post_init__(self):
        """Validações pós-inicialização"""
        # Não pode depender de si mesmo
        if self.successor_id == self.predecessor_id:
            raise ValueError("Um item não pode depender de si mesmo")
        
        # Lag deve ser um número razoável
        if abs(self.lag_days) > 365:
            raise ValueError("Lag de dependência deve estar entre -365 e +365 dias")
    
    def is_finish_to_start(self) -> bool:
        """Verifica se é dependência Finish-to-Start (mais comum)"""
        return self.dependency_type == DependencyType.FINISH_TO_START
    
    def has_lag(self) -> bool:
        """Verifica se tem lag (atraso ou antecipação)"""
        return self.lag_days != 0
    
    def is_positive_lag(self) -> bool:
        """Verifica se o lag é positivo (esperar dias extras)"""
        return self.lag_days > 0
    
    def is_negative_lag(self) -> bool:
        """Verifica se o lag é negativo (sobreposição)"""
        return self.lag_days < 0
    
    def get_description(self) -> str:
        """Retorna descrição legível da dependência"""
        pred_name = self.predecessor_name or f"Item {self.predecessor_id}"
        succ_name = self.successor_name or f"Item {self.successor_id}"
        
        desc = f"'{succ_name}' depende de '{pred_name}' ({self.dependency_type.get_display_name()})"
        
        if self.has_lag():
            if self.is_positive_lag():
                desc += f" com espera de {self.lag_days} dias"
            else:
                desc += f" com sobreposição de {abs(self.lag_days)} dias"
        
        return desc

