from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.data.use_cases.get_count_projects_by_fiscal import GetCountProjectsByFiscal
from src.presentation.controllers.get_count_projects_by_fiscal_controller import GetCountProjectsByFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_count_projects_by_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetCountProjectsByFiscalController(
        get_count_projects_by_fiscal=GetCountProjectsByFiscal(
            project_fiscal_repository=ProjectFiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle