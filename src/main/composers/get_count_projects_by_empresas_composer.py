from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.get_count_projects_by_empresas import GetCountProjectsByEmpresas
from src.presentation.controllers.get_count_projects_by_empresas_controller import GetCountProjectsByEmpresasController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_count_projects_by_empresas_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetCountProjectsByEmpresasController(
        get_count_projects_by_empresas=GetCountProjectsByEmpresas(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle