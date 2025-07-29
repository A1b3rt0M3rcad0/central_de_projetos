"""
Composer responsável por montar a cadeia de dependências para o endpoint de atualização do nome do fiscal.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case UpdateFiscalName
- Instancia o controller UpdateFiscalNameController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.update_fiscal_name import UpdateFiscalName
from src.presentation.controllers.update_fiscal_name_controller import UpdateFiscalNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_fiscal_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateFiscalNameController(
        update_fiscal_name_case=UpdateFiscalName(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle