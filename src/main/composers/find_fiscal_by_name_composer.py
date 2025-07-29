"""
Composer responsável por montar a cadeia de dependências para o endpoint de busca de fiscal por nome.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case FindFiscalByName
- Instancia o controller FindFiscalByNameController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.find_fiscal_by_name import FindFiscalByName
from src.presentation.controllers.find_fiscal_by_name_controller import FindFiscalByNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_fiscal_by_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindFiscalByNameController(
        find_fiscal_by_name_case=FindFiscalByName(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle