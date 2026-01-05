"""Caso de uso para deletar dependência entre itens da EAP"""
from src.domain.use_cases.i_delete_eap_dependency import IDeleteEAPDependency
from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository


class DeleteEAPDependency(IDeleteEAPDependency):
    """Implementação do caso de uso de deletar dependência"""
    
    def __init__(self, dependency_repository: IEAPDependencyRepository):
        self.__dependency_repository = dependency_repository
    
    def delete(self, dependency_id: int) -> None:
        """
        Remove uma dependência entre itens da EAP
        
        Raises:
            ValueError: Se a dependência não existir
        """
        # Verifica se a dependência existe
        dependency = self.__dependency_repository.find_by_id(dependency_id)
        if not dependency:
            raise ValueError(f"Dependência com ID {dependency_id} não encontrada")
        
        # Deleta
        self.__dependency_repository.delete(dependency_id)

