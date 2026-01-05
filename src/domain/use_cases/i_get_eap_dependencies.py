"""Interface para buscar dependências de um item da EAP"""
from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.eap_dependency import EAPDependencyEntity


class IGetEAPDependencies(ABC):
    """Interface para buscar dependências de um item"""
    
    @abstractmethod
    def get_by_item(self, item_id: int) -> dict:
        """
        Busca todas as dependências relacionadas a um item
        
        Args:
            item_id: ID do item da EAP
            
        Returns:
            dict com:
                - predecessors: Lista de itens que este item depende
                - successors: Lista de itens que dependem deste item
                
        Raises:
            EAPItemNotFoundError: Se o item não existir
        """
        pass
    
    @abstractmethod
    def get_all_by_eap(self, eap_id: int) -> List[EAPDependencyEntity]:
        """
        Busca todas as dependências de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPDependencyEntity]: Lista de todas as dependências
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
        """
        pass

