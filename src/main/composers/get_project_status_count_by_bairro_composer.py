from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.data.use_cases.get_project_status_count_by_bairro import GetProjectStatusCountByBairro
from src.presentation.controllers.get_project_status_count_by_bairro_controller import GetProjectStatusCountByBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_project_status_count_by_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectStatusCountByBairroController(
        get_project_status_caount_by_bairro=GetProjectStatusCountByBairro(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle