from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_projects_from_fiscal import FindAllProjectsFromFiscal
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.find_all_projects_from_fiscal_controller import FindAllProjectsFromFiscalController
from src.presentation.http_types.http_request import  HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_from_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllProjectsFromFiscalController(
        find_all_projects_from_fiscal_case=FindAllProjectsFromFiscal(
            project_fiscal_repository=ProjectFiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle