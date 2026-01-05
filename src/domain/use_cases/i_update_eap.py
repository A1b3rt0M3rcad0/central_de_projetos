from abc import ABC, abstractmethod
from typing import Optional

from ..entities.eap import EAPEntity


class IUpdateEAP(ABC):
    """Interface para o caso de uso de atualização de EAP"""
    
    @abstractmethod
    def update(self, eap_id: int, name: Optional[str] = None, description: Optional[str] = None) -> EAPEntity:
        """
        Atualiza os dados básicos de uma EAP
        
        Args:
            eap_id: ID da EAP
            name: Novo nome da EAP (opcional)
            description: Nova descrição da EAP (opcional)
            
        Returns:
            EAPEntity: A EAP atualizada
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
            ValueError: Se os dados fornecidos forem inválidos
        """
        pass
