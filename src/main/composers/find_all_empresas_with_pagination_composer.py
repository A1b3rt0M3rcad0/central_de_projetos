from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.find_all_empresas_with_pagination import FindAllEmpresasWithPagination
from src.presentation.controllers.find_all_empresas_with_pagination_controller import FindAllEmpresasWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_empresas_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllEmpresasWithPaginationController(
        find_all_empresas_with_pagination_case=FindAllEmpresasWithPagination(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
