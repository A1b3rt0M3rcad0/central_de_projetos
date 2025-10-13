"""Interface para deletar dependência entre itens da EAP"""
from abc import ABC, abstractmethod


class IDeleteEAPDependency(ABC):
    """Interface para o caso de uso de deleção de dependência"""
    
    @abstractmethod
    def delete(self, dependency_id: int) -> None:
        """
        Remove uma dependência entre itens da EAP
        
        Args:
            dependency_id: ID da dependência a ser removida
            
        Raises:
            DependencyNotFoundError: Se a dependência não existir
            ErrorOnDeleteDependency: Se ocorrer erro ao deletar
        """
        pass

