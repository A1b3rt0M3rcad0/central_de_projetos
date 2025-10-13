"""Caso de uso para criar dependência entre itens da EAP"""
from datetime import datetime, timezone
from src.domain.use_cases.i_create_eap_dependency import ICreateEAPDependency
from src.domain.entities.eap_dependency import EAPDependencyEntity
from src.domain.value_objects.dependency_type import DependencyType
from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository
from src.data.interface.i_eap_item_repository import IEAPItemRepository


class CreateEAPDependency(ICreateEAPDependency):
    """Implementação do caso de uso de criar dependência"""
    
    def __init__(
        self, 
        dependency_repository: IEAPDependencyRepository,
        eap_item_repository: IEAPItemRepository
    ):
        self.__dependency_repository = dependency_repository
        self.__eap_item_repository = eap_item_repository
    
    def create(
        self,
        successor_id: int,
        predecessor_id: int,
        dependency_type: DependencyType = DependencyType.FINISH_TO_START,
        lag_days: int = 0
    ) -> EAPDependencyEntity:
        """
        Cria uma nova dependência entre itens da EAP
        
        Validações:
        1. Verifica se ambos os itens existem
        2. Não pode depender de si mesmo
        3. Não pode criar dependência circular
        4. Não pode depender de descendentes na hierarquia
        5. Não pode duplicar dependência
        """
        
        # Validação 1: Verificar se os itens existem
        successor = self.__eap_item_repository.find_by_id(successor_id)
        if not successor:
            raise ValueError(f"Item sucessor com ID {successor_id} não encontrado")
        
        predecessor = self.__eap_item_repository.find_by_id(predecessor_id)
        if not predecessor:
            raise ValueError(f"Item predecessor com ID {predecessor_id} não encontrado")
        
        # Validação 2: Não pode depender de si mesmo
        if successor_id == predecessor_id:
            raise ValueError("Um item não pode depender de si mesmo")
        
        # Validação 3: Verificar ciclo circular
        if self.__dependency_repository.has_circular_dependency(successor_id, predecessor_id):
            raise ValueError(
                f"Criar esta dependência geraria um ciclo circular. "
                f"'{successor.name}' já depende indiretamente de '{predecessor.name}'"
            )
        
        # Validação 4: Predecessor não pode ser descendente do successor
        if self.__dependency_repository.is_descendant(predecessor_id, successor_id):
            raise ValueError(
                f"Não é possível: '{predecessor.name}' é descendente de '{successor.name}' "
                f"na hierarquia da EAP"
            )
        
        # Validação 5: Verificar se já existe
        if self.__dependency_repository.exists(successor_id, predecessor_id):
            raise ValueError(
                f"Já existe uma dependência entre '{successor.name}' e '{predecessor.name}'"
            )
        
        # Criar entidade de dependência
        dependency_entity = EAPDependencyEntity(
            id=None,
            successor_id=successor_id,
            predecessor_id=predecessor_id,
            dependency_type=dependency_type,
            lag_days=lag_days,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            successor_name=successor.name,
            successor_code=successor.code.value if hasattr(successor.code, 'value') else str(successor.code),
            predecessor_name=predecessor.name,
            predecessor_code=predecessor.code.value if hasattr(predecessor.code, 'value') else str(predecessor.code)
        )
        
        # Salvar no repositório
        return self.__dependency_repository.create(dependency_entity)

