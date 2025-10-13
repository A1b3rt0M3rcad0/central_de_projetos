"""Interface para criar dependência entre itens da EAP"""
from abc import ABC, abstractmethod
from src.domain.entities.eap_dependency import EAPDependencyEntity
from src.domain.value_objects.dependency_type import DependencyType


class ICreateEAPDependency(ABC):
    """Interface para o caso de uso de criação de dependência"""
    
    @abstractmethod
    def create(
        self, 
        successor_id: int,
        predecessor_id: int,
        dependency_type: DependencyType = DependencyType.FINISH_TO_START,
        lag_days: int = 0
    ) -> EAPDependencyEntity:
        """
        Cria uma nova dependência entre dois itens da EAP
        
        Args:
            successor_id: ID do item que depende (sucessor)
            predecessor_id: ID do item do qual depende (predecessor)
            dependency_type: Tipo de dependência (padrão: FS)
            lag_days: Atraso em dias (padrão: 0)
            
        Returns:
            EAPDependencyEntity: A dependência criada
            
        Raises:
            EAPItemNotFoundError: Se algum dos itens não existir
            SelfDependencyError: Se tentar criar dependência de um item consigo mesmo
            CircularDependencyError: Se criar dependência circular
            DescendantDependencyError: Se predecessor for descendente do successor
            DuplicateDependencyError: Se a dependência já existir
            InvalidDependencyTypeError: Se o tipo de dependência for inválido
        """
        pass

