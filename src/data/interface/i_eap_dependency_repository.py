"""Interface do repositório de dependências de EAP"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.eap_dependency import EAPDependencyEntity


class IEAPDependencyRepository(ABC):
    """Interface para repositório de dependências entre itens da EAP"""
    
    @abstractmethod
    def create(self, dependency: EAPDependencyEntity) -> EAPDependencyEntity:
        """
        Cria uma nova dependência
        
        Args:
            dependency: Entidade de dependência a ser criada
            
        Returns:
            EAPDependencyEntity: Dependência criada com ID
        """
        pass
    
    @abstractmethod
    def find_by_id(self, dependency_id: int) -> Optional[EAPDependencyEntity]:
        """
        Busca uma dependência por ID
        
        Args:
            dependency_id: ID da dependência
            
        Returns:
            Optional[EAPDependencyEntity]: Dependência encontrada ou None
        """
        pass
    
    @abstractmethod
    def find_predecessors(self, item_id: int) -> List[EAPDependencyEntity]:
        """
        Busca todos os predecessores de um item (itens dos quais ele depende)
        
        Args:
            item_id: ID do item sucessor
            
        Returns:
            List[EAPDependencyEntity]: Lista de dependências onde item é sucessor
        """
        pass
    
    @abstractmethod
    def find_successors(self, item_id: int) -> List[EAPDependencyEntity]:
        """
        Busca todos os sucessores de um item (itens que dependem dele)
        
        Args:
            item_id: ID do item predecessor
            
        Returns:
            List[EAPDependencyEntity]: Lista de dependências onde item é predecessor
        """
        pass
    
    @abstractmethod
    def find_all_by_eap(self, eap_id: int) -> List[EAPDependencyEntity]:
        """
        Busca todas as dependências de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPDependencyEntity]: Lista de todas as dependências
        """
        pass
    
    @abstractmethod
    def exists(self, successor_id: int, predecessor_id: int) -> bool:
        """
        Verifica se uma dependência já existe
        
        Args:
            successor_id: ID do sucessor
            predecessor_id: ID do predecessor
            
        Returns:
            bool: True se a dependência existe
        """
        pass
    
    @abstractmethod
    def delete(self, dependency_id: int) -> None:
        """
        Remove uma dependência
        
        Args:
            dependency_id: ID da dependência a ser removida
        """
        pass
    
    @abstractmethod
    def has_circular_dependency(self, successor_id: int, predecessor_id: int) -> bool:
        """
        Verifica se criar esta dependência geraria um ciclo
        
        Exemplo de ciclo: A → B → C → A
        
        Args:
            successor_id: ID do sucessor
            predecessor_id: ID do predecessor
            
        Returns:
            bool: True se criar dependência geraria ciclo
        """
        pass
    
    @abstractmethod
    def is_descendant(self, potential_descendant_id: int, ancestor_id: int) -> bool:
        """
        Verifica se um item é descendente de outro na hierarquia da EAP
        
        Args:
            potential_descendant_id: ID do possível descendente
            ancestor_id: ID do possível ancestral
            
        Returns:
            bool: True se potential_descendant é filho/neto/etc de ancestor
        """
        pass

