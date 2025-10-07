"""Get System Config Composer"""
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.system_config_repository import SystemConfigRepository
from src.data.use_cases.get_system_config import GetSystemConfig
from src.presentation.controllers.get_system_config_controller import GetSystemConfigController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


def get_system_config_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar configurações do sistema"""
    
    return GetSystemConfigController(
        get_system_config_use_case=GetSystemConfig(
            system_config_repository=SystemConfigRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

