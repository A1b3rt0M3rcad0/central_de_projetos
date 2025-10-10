from typing import Dict, Any
from src.domain.use_cases.i_delete_eap_item import IDeleteEAPItem
from src.errors.http.__http_base_error import HttpBaseError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class DeleteEAPItemController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para exclusão de item da EAP"""
    
    def __init__(self, delete_eap_item_case: IDeleteEAPItem):
        self.__delete_eap_item_case = delete_eap_item_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Manipula a requisição de exclusão de item da EAP
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        try:
            # Valida se o item_id foi fornecido
            item_id = http_request.path_params.get('item_id')
            if not item_id:
                return HttpResponse(
                    status_code=400,
                    body={"error": "ID do item é obrigatório"}
                )
            
            # Converte para int
            try:
                item_id = int(item_id)
            except ValueError:
                return HttpResponse(
                    status_code=400,
                    body={"error": "ID do item deve ser um número válido"}
                )
            
            # Executa a exclusão
            self.__delete_eap_item_case.delete(item_id)
            
            return HttpResponse(
                status_code=200,
                body={"message": "Item da EAP excluído com sucesso"}
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
