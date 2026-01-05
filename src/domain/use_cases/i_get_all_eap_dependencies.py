"""Interface para buscar TODAS as dependências de uma EAP"""
from abc import ABC, abstractmethod
from typing import Dict


class IGetAllEAPDependencies(ABC):
    """Interface para buscar todas as dependências de uma EAP de uma só vez"""
    
    @abstractmethod
    def get_all_by_eap(self, eap_id: int) -> Dict[int, dict]:
        """
        Busca todas as dependências de todos os itens de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            Dict com item_id como chave e dict com predecessors/successors como valor
        """

