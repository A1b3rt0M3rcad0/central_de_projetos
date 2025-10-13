"""Caso de uso para buscar TODAS as dependências de uma EAP de uma vez"""
from typing import Dict
from src.domain.use_cases.i_get_all_eap_dependencies import IGetAllEAPDependencies
from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository
from src.data.interface.i_eap_repository import IEAPRepository


class GetAllEAPDependencies(IGetAllEAPDependencies):
    """Implementação do caso de uso de buscar TODAS as dependências de uma EAP"""
    
    def __init__(
        self, 
        dependency_repository: IEAPDependencyRepository,
        eap_repository: IEAPRepository
    ):
        self.__dependency_repository = dependency_repository
        self.__eap_repository = eap_repository
    
    def get_all_by_eap(self, eap_id: int) -> Dict[int, dict]:
        """
        Busca TODAS as dependências de todos os itens de uma EAP de uma só vez
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            Dict com item_id como chave e dict com predecessors/successors como valor
        """
        # Verifica se a EAP existe
        eap = self.__eap_repository.find_by_id(eap_id)
        if not eap:
            raise ValueError(f"EAP com ID {eap_id} não encontrada")
        
        # Busca todos os itens da EAP
        items = eap.items if hasattr(eap, 'items') and eap.items else []
        
        # Inicializa dicionário de resposta
        dependencies_by_item = {}
        
        # Para cada item, busca suas dependências
        for item in items:
            item_id = item.id
            
            # Busca predecessores (itens dos quais este item depende)
            predecessors = self.__dependency_repository.find_predecessors(item_id)
            
            # Busca sucessores (itens que dependem deste item)
            successors = self.__dependency_repository.find_successors(item_id)
            
            # Armazena no dicionário
            dependencies_by_item[item_id] = {
                "predecessors": predecessors,
                "successors": successors
            }
        
        return dependencies_by_item

