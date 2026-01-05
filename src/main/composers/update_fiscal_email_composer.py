"""
Composer responsável por montar a cadeia de dependências para o endpoint de atualização do email do fiscal.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case UpdateFiscalEmail
- Instancia o controller UpdateFiscalEmailController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.update_fiscal_email import UpdateFiscalEmail
from src.presentation.controllers.update_fiscal_email_controller import UpdateFiscalEmailController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_fiscal_email_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateFiscalEmailController(
        update_fiscal_email_case=UpdateFiscalEmail(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

