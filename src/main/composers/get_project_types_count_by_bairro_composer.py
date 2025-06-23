from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.data.use_cases.get_project_types_count_by_bairro import GetProjectTypesCountByBairro
from src.presentation.controllers.get_project_types_count_by_bairro_controller import GetProjectTypesCountByBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_project_types_count_by_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectTypesCountByBairroController(
        get_project_types_count_by_bairro=GetProjectTypesCountByBairro(
            project_type_repository=ProjectTypeRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle