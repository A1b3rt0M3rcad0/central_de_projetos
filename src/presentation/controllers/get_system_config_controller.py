#pylint:disable=all
"""Get System Config Controller"""
from src.domain.use_cases.i_get_system_config import IGetSystemConfig
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GetSystemConfigController(ControllerInterface):
    """Controller para buscar configurações do sistema"""
    
    def __init__(self, get_system_config_use_case: IGetSystemConfig) -> None:
        self.__get_system_config_use_case = get_system_config_use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição de configurações do sistema
        
        Query params aceitos:
            - config_key: Chave específica (opcional)
        """
        try:
            query_params = http_request.query_params
            config_key = query_params.get('config_key')
            
            result = self.__get_system_config_use_case.execute(config_key)
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'System configurations retrieved successfully',
                    'content': result
                }
            )
        except Exception as e:
            raise e from e

