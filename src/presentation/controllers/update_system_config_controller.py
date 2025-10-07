#pylint:disable=all
"""Update System Config Controller"""
from src.domain.use_cases.i_update_system_config import IUpdateSystemConfig
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class UpdateSystemConfigController(ControllerInterface):
    """Controller para atualizar configurações do sistema"""
    
    def __init__(self, update_system_config_use_case: IUpdateSystemConfig) -> None:
        self.__update_system_config_use_case = update_system_config_use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição de atualização de configuração
        
        Body esperado:
            {
                "config_key": "dashboard.excluded_status",
                "config_value": "[13,14]"
            }
        """
        try:
            body = http_request.body
            config_key = body.get('config_key')
            config_value = body.get('config_value')
            
            if not config_key or config_value is None:
                raise ValueError("config_key and config_value are required")
            
            self.__update_system_config_use_case.execute(config_key, config_value)
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'System configuration updated successfully',
                    'content': {
                        'config_key': config_key,
                        'config_value': config_value
                    }
                }
            )
        except Exception as e:
            raise e from e

