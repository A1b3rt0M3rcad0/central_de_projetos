"""Controller para buscar dependências de itens da EAP"""
from src.domain.use_cases.i_get_eap_dependencies import IGetEAPDependencies
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GetEAPDependenciesController(ControllerInterface):
    """Controller para busca de dependências"""
    
    def __init__(self, use_case: IGetEAPDependencies):
        self.__use_case = use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição para buscar dependências de um item
        
        Args:
            http_request: HttpRequest com item_id nos path_params
            
        Returns:
            HttpResponse
        """
        try:
            # Extrai item_id dos path params
            path_params = http_request.path_params
            item_id = int(path_params["item_id"])
            
            # Executa use case
            result = self.__use_case.get_by_item(item_id)
            
            # Formata predecessores
            predecessors_formatted = []
            for dep in result["predecessors"]:
                predecessors_formatted.append({
                    "dependency_id": dep.id,
                    "predecessor_id": dep.predecessor_id,
                    "predecessor_name": dep.predecessor_name,
                    "predecessor_code": dep.predecessor_code,
                    "type": dep.dependency_type.value,
                    "type_label": dep.dependency_type.get_display_name(),
                    "lag_days": dep.lag_days
                })
            
            # Formata sucessores
            successors_formatted = []
            for dep in result["successors"]:
                successors_formatted.append({
                    "dependency_id": dep.id,
                    "successor_id": dep.successor_id,
                    "successor_name": dep.successor_name,
                    "successor_code": dep.successor_code,
                    "type": dep.dependency_type.value,
                    "type_label": dep.dependency_type.get_display_name(),
                    "lag_days": dep.lag_days
                })
            
            # Retorna resposta
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Dependências encontradas",
                    "content": {
                        "item_id": result["item_id"],
                        "item_name": result["item_name"],
                        "item_code": result["item_code"],
                        "predecessors": predecessors_formatted,
                        "successors": successors_formatted,
                        "total_predecessors": len(predecessors_formatted),
                        "total_successors": len(successors_formatted)
                    }
                }
            )
            
        except Exception as error:
            raise error from error

