"""Get Dashboard Data Composer"""
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.dashboard_repository import DashboardRepository
from src.infra.relational.repository.system_config_repository import SystemConfigRepository
from src.data.use_cases.get_dashboard_data import GetDashboardData
from src.presentation.controllers.get_dashboard_data_controller import GetDashboardDataController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


def get_dashboard_data_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar dados do dashboard"""
    
    db_handler = db_connection_handler_factory()
    
    return GetDashboardDataController(
        get_dashboard_data_use_case=GetDashboardData(
            dashboard_repository=DashboardRepository(
                db_connection_handler=db_handler
            ),
            system_config_repository=SystemConfigRepository(
                db_connection_handler=db_handler
            )
        )
    ).handle

