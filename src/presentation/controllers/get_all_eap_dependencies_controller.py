"""Controller para buscar TODAS as dependências de uma EAP de uma vez"""
from src.domain.use_cases.i_get_all_eap_dependencies import IGetAllEAPDependencies
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GetAllEAPDependenciesController(ControllerInterface):
    """Controller para busca de todas as dependências de uma EAP"""
    
    def __init__(self, use_case: IGetAllEAPDependencies):
        self.__use_case = use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição para buscar TODAS as dependências de uma EAP
        
        Args:
            http_request: HttpRequest com eap_id nos path_params
            
        Returns:
            HttpResponse com dicionário de dependências por item
        """
        try:
            # Extrai eap_id dos path params
            path_params = http_request.path_params
            eap_id = int(path_params["eap_id"])
            
            # Executa use case
            result = self.__use_case.get_all_by_eap(eap_id)
            
            # Formata resultado
            dependencies_by_item = {}
            
            for item_id, deps in result.items():
                # Formata predecessores
                predecessors_formatted = []
                for dep in deps["predecessors"]:
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
                for dep in deps["successors"]:
                    successors_formatted.append({
                        "dependency_id": dep.id,
                        "successor_id": dep.successor_id,
                        "successor_name": dep.successor_name,
                        "successor_code": dep.successor_code,
                        "type": dep.dependency_type.value,
                        "type_label": dep.dependency_type.get_display_name(),
                        "lag_days": dep.lag_days
                    })
                
                dependencies_by_item[str(item_id)] = {
                    "item_id": item_id,
                    "predecessors": predecessors_formatted,
                    "successors": successors_formatted
                }
            
            # Retorna resposta
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Todas as dependências da EAP encontradas",
                    "content": dependencies_by_item
                }
            )
            
        except Exception as error:
            raise error from error

