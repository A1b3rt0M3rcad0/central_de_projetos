"""
Composer responsável por montar a cadeia de dependências para o endpoint de criação de fiscal a partir de todos os dados de usuário.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case InsertAllFiscalFromFiscalUseCase
- Instancia o controller InsertAllFiscalFromFiscalController
- Retorna o método handle do controller
"""

from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.data.use_cases.insert_all_fiscal_from_user import InsertAllFiscalFromFiscalUseCase
from src.presentation.controllers.insert_all_fiscal_from_user_controller import InsertAllFiscalFromFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def insert_all_fiscal_from_user_composer() -> Callable[[HttpRequest], HttpResponse]:
    return InsertAllFiscalFromFiscalController(
        InsertAllFiscalFromFiscalUseCase(
            FiscalRepository(
                db_connection_handler_factory()
            )
        )
    ).handle
