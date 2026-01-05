"""Update System Config Composer"""
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.system_config_repository import SystemConfigRepository
from src.data.use_cases.update_system_config import UpdateSystemConfig
from src.presentation.controllers.update_system_config_controller import UpdateSystemConfigController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


def update_system_config_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de atualizar configurações do sistema"""
    
    return UpdateSystemConfigController(
        update_system_config_use_case=UpdateSystemConfig(
            system_config_repository=SystemConfigRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

