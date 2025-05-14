from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_projects_from_bairro import FindAllProjectsFromBairro
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.find_all_projects_from_bairro_controller import FindAllProjectsFromBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_from_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllProjectsFromBairroController(
        find_all_projects_from_bairro_case=FindAllProjectsFromBairro(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle