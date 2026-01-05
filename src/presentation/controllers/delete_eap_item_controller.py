from typing import Dict, Any
from src.domain.use_cases.i_delete_eap_item import IDeleteEAPItem
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_find_eap_item import IFindEAPItem
from src.domain.use_cases.i_find_eap import IFindEAP
from src.errors.http.__http_base_error import HttpBaseError
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class DeleteEAPItemController(ControllerInterface):  # pylint: disable=too-few-public-methods
    """Controller para exclusão de item da EAP"""
    
    def __init__(self, delete_eap_item_case: IDeleteEAPItem, create_history_case: ICreateHistoryProject, find_eap_item_case: IFindEAPItem, find_eap_case: IFindEAP):
        self.__delete_eap_item_case = delete_eap_item_case
        self.__create_history_case = create_history_case
        self.__find_eap_item_case = find_eap_item_case
        self.__find_eap_case = find_eap_case
    
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
            
            # Busca informações do item antes de deletar (para o histórico)
            try:
                item = self.__find_eap_item_case.find_by_id(item_id)
                item_name = item.name if item else "desconhecido"
                item_code = str(item.code) if item else "desconhecido"
                eap_id = item.eap_id if item else None
            except Exception:
                item_name = "desconhecido"
                item_code = "desconhecido"
                eap_id = None
            
            # Executa a exclusão
            self.__delete_eap_item_case.delete(item_id)
            
            # Registra no histórico do projeto
            if eap_id:
                try:
                    eap = self.__find_eap_case.find_by_id(eap_id)
                    if eap and eap.project_id:
                        self.__create_history_case.create(
                            project_id=eap.project_id,
                            data_name="Item EAP",
                            description=f"Item EAP '{item_name}' (código {item_code}) deletado"
                        )
                except Exception:
                    # Se falhar ao criar histórico, não bloqueia a operação principal
                    pass
            
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
