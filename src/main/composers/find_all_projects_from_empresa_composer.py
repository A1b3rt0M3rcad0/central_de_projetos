from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_projects_from_empresa import FindAllProjectsFromEmpresa
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.find_all_projects_from_empresa_controller import FindAllProjectsFromEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_from_empresa_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_handler = db_connection_handler_factory()
    return FindAllProjectsFromEmpresaController(
        find_all_projects_from_empresa_case=FindAllProjectsFromEmpresa(
            project_empresa_repository=ProjectEmpresaRepository(
                db_connection_handler=db_handler
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_handler
            )
        )
    ).handle