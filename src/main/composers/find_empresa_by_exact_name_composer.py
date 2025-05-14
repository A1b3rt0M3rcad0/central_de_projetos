from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.find_empresa_by_exact_name import FindEmpresaByExactName
from src.presentation.controllers.find_empresa_by_exact_name_controller import FindEmpresaByExactNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_empresa_by_exact_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindEmpresaByExactNameController(
        find_empresa_by_exact_name_case=FindEmpresaByExactName(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle