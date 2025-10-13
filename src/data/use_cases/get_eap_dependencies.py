"""Caso de uso para buscar dependências de itens da EAP"""
from typing import List
from src.domain.use_cases.i_get_eap_dependencies import IGetEAPDependencies
from src.domain.entities.eap_dependency import EAPDependencyEntity
from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.data.interface.i_eap_repository import IEAPRepository


class GetEAPDependencies(IGetEAPDependencies):
    """Implementação do caso de uso de buscar dependências"""
    
    def __init__(
        self, 
        dependency_repository: IEAPDependencyRepository,
        eap_item_repository: IEAPItemRepository,
        eap_repository: IEAPRepository
    ):
        self.__dependency_repository = dependency_repository
        self.__eap_item_repository = eap_item_repository
        self.__eap_repository = eap_repository
    
    def get_by_item(self, item_id: int) -> dict:
        """
        Busca todas as dependências relacionadas a um item
        
        Retorna dict com:
        - predecessors: Itens dos quais este item depende
        - successors: Itens que dependem deste item
        """
        # Verifica se o item existe
        item = self.__eap_item_repository.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item com ID {item_id} não encontrado")
        
        # Busca predecessores (itens dos quais este item depende)
        predecessors = self.__dependency_repository.find_predecessors(item_id)
        
        # Busca sucessores (itens que dependem deste item)
        successors = self.__dependency_repository.find_successors(item_id)
        
        return {
            "item_id": item_id,
            "item_name": item.name,
            "item_code": item.code.value if hasattr(item.code, 'value') else str(item.code),
            "predecessors": predecessors,
            "successors": successors
        }
    
    def get_all_by_eap(self, eap_id: int) -> List[EAPDependencyEntity]:
        """Busca todas as dependências de uma EAP"""
        # Verifica se a EAP existe
        eap = self.__eap_repository.find_by_id(eap_id)
        if not eap:
            raise ValueError(f"EAP com ID {eap_id} não encontrada")
        
        # Busca todas as dependências
        return self.__dependency_repository.find_all_by_eap(eap_id)

