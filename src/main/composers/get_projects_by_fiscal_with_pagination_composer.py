"""
Composer responsável por montar a cadeia de dependências para o endpoint de busca de projetos de um fiscal com paginação.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia ProjectFiscalRepository com o handler de conexão
- Instancia ProjectRepository com o handler de conexão
- Instancia o use case GetProjectsByFiscalWithPagination
- Instancia o use case FindProject
- Instancia o controller GetProjectsByFiscalWithPaginationController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.data.use_cases.get_projects_by_fiscal_with_pagination import GetProjectsByFiscalWithPagination
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.get_projects_by_fiscal_with_pagination_controller import GetProjectsByFiscalWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_projects_by_fiscal_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectsByFiscalWithPaginationController(
        get_projects_by_fiscal_with_pagination=GetProjectsByFiscalWithPagination(
            project_fiscal_repository=ProjectFiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        work_project_repository=WorkProjectRepository(
            db_connection_handler=db_connection_handler_factory()
        )
    ).handle 