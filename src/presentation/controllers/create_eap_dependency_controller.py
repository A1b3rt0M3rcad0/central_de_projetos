"""Controller para criar dependência entre itens da EAP"""
from src.domain.use_cases.i_create_eap_dependency import ICreateEAPDependency
from src.domain.value_objects.dependency_type import DependencyType
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class CreateEAPDependencyController(ControllerInterface):
    """Controller para criação de dependências"""
    
    def __init__(self, use_case: ICreateEAPDependency):
        self.__use_case = use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição para criar dependência
        
        Args:
            http_request: HttpRequest com body contendo:
                - successor_id: int
                - predecessor_id: int
                - dependency_type: str (opcional)
                - lag_days: int (opcional)
            
        Returns:
            HttpResponse
        """
        try:
            # Extrai dados do request
            body = http_request.body
            successor_id = body.get("successor_id")
            predecessor_id = body.get("predecessor_id")
            dependency_type_str = body.get("dependency_type", "FS")
            lag_days = body.get("lag_days", 0)
            
            # Converte tipo de dependência
            dependency_type = DependencyType.from_string(dependency_type_str)
            
            # Executa use case
            dependency = self.__use_case.create(
                successor_id=int(successor_id),
                predecessor_id=int(predecessor_id),
                dependency_type=dependency_type,
                lag_days=int(lag_days)
            )
            
            # Retorna resposta de sucesso
            return HttpResponse(
                status_code=201,
                body={
                    "message": "Dependência criada com sucesso",
                    "content": {
                        "id": dependency.id,
                        "successor_id": dependency.successor_id,
                        "successor_name": dependency.successor_name,
                        "successor_code": dependency.successor_code,
                        "predecessor_id": dependency.predecessor_id,
                        "predecessor_name": dependency.predecessor_name,
                        "predecessor_code": dependency.predecessor_code,
                        "dependency_type": dependency.dependency_type.value,
                        "dependency_type_label": dependency.dependency_type.get_display_name(),
                        "lag_days": dependency.lag_days,
                        "created_at": dependency.created_at.isoformat() if dependency.created_at else None
                    }
                }
            )
            
        except Exception as error:
            raise error from error

