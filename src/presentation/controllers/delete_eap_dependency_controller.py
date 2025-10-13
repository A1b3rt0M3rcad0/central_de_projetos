"""Controller para deletar dependência entre itens da EAP"""
from src.domain.use_cases.i_delete_eap_dependency import IDeleteEAPDependency
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class DeleteEAPDependencyController(ControllerInterface):
    """Controller para deleção de dependências"""
    
    def __init__(self, use_case: IDeleteEAPDependency):
        self.__use_case = use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição para deletar uma dependência
        
        Args:
            http_request: HttpRequest com dependency_id nos path_params
            
        Returns:
            HttpResponse
        """
        try:
            # Extrai dependency_id dos path params
            path_params = http_request.path_params
            dependency_id = int(path_params["dependency_id"])
            
            # Executa use case
            self.__use_case.delete(dependency_id)
            
            # Retorna resposta de sucesso
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Dependência removida com sucesso"
                }
            )
            
        except Exception as error:
            raise error from error

