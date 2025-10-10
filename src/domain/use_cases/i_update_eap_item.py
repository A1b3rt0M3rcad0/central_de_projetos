from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from ..entities.eap import EAPItemEntity
from ..value_objects.eap_status import EAPStatus
from ..value_objects.monetary_value import MonetaryValue


class IUpdateEAPItem(ABC):
    """Interface para o caso de uso de atualização de item da EAP"""
    
    @abstractmethod
    def update(self, item_id: int, name: Optional[str] = None, description: Optional[str] = None,
               responsible: Optional[str] = None, start_date: Optional[datetime] = None,
               end_date: Optional[datetime] = None, budget: Optional[MonetaryValue] = None,
               status: Optional[EAPStatus] = None, progress: Optional[int] = None) -> EAPItemEntity:
        """
        Atualiza um item da EAP
        
        Args:
            item_id: ID do item
            name: Novo nome do item (opcional)
            description: Nova descrição do item (opcional)
            responsible: Novo responsável (opcional)
            start_date: Nova data de início (opcional)
            end_date: Nova data de fim (opcional)
            budget: Novo orçamento (opcional)
            status: Novo status (opcional)
            progress: Novo progresso (opcional)
            
        Returns:
            EAPItemEntity: O item atualizado
            
        Raises:
            EAPItemNotFoundError: Se o item não existir
            ValueError: Se os dados fornecidos forem inválidos
            InvalidStatusTransitionError: Se a transição de status for inválida
        """
        pass
