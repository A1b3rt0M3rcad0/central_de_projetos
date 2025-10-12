"""Get Gantt Data Controller"""
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_gantt_data import IGetGanttData
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class GetGanttDataController(ControllerInterface):
    """Controller para buscar dados do Gantt Chart"""
    
    def __init__(self, get_gantt_data_case: IGetGanttData) -> None:
        self.__get_gantt_data_case = get_gantt_data_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Manipula a requisição de busca de dados do Gantt
        
        Args:
            http_request: Requisição HTTP
            
        Returns:
            HttpResponse: Resposta HTTP com dados do Gantt
        """
        try:
            # Extrair project_id dos path params
            project_id = http_request.path_params.get('project_id')
            
            if not project_id:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'project_id é obrigatório'}
                )
            
            # Executar caso de uso
            gantt_data = self.__get_gantt_data_case.execute(int(project_id))
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Dados do Gantt Chart obtidos com sucesso',
                    'content': gantt_data
                }
            )
            
        except ProjectNotFoundError as error:
            return HttpResponse(
                status_code=404,
                body={'error': error.message}
            )
        except EAPNotFoundError as error:
            return HttpResponse(
                status_code=error.status_code,
                body={'error': error.message}
            )
        except ValueError as error:
            return HttpResponse(
                status_code=400,
                body={'error': f'Erro de validação: {str(error)}'}
            )
        except Exception as error:
            return HttpResponse(
                status_code=500,
                body={'error': f'Erro interno: {str(error)}'}
            )

