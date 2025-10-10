from typing import Dict, Any
from src.domain.use_cases.i_delete_eap import IDeleteEAP
from src.errors.http.__http_base_error import HttpBaseError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class DeleteEAPController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para exclusão de EAP"""
    
    def __init__(self, delete_eap_case: IDeleteEAP):
        self.__delete_eap_case = delete_eap_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Manipula a requisição de exclusão de EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            # Valida se o eap_id foi fornecido
            eap_id = http_request.path_params.get('eap_id')
            if not eap_id:
                return HttpResponse(
                    status_code=400,
                    body={"error": "ID da EAP é obrigatório"}
                )
            
            # Converte para int
            try:
                eap_id = int(eap_id)
            except ValueError:
                return HttpResponse(
                    status_code=400,
                    body={"error": "ID da EAP deve ser um número válido"}
                )
            
            # Executa a exclusão
            self.__delete_eap_case.delete(eap_id)
            
            return HttpResponse(
                status_code=200,
                body={"message": "EAP excluída com sucesso"}
            )
            
        except HttpBaseError as exc:
            return HttpResponse(
                status_code=exc.status_code,
                body={"error": exc.message}
            )
        except Exception as exc:
            return HttpResponse(
                status_code=500,
                body={"error": f"Erro interno do servidor: {str(exc)}"}
            )
