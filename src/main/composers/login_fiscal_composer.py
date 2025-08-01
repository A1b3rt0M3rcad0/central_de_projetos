from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.login_fiscal import LoginFiscal
from src.data.use_cases.create_refresh_token_fiscal import CreateRefreshTokenFiscal
from src.data.use_cases.update_refresh_token_fiscal import UpdateRefreshTokenFiscal
from src.presentation.controllers.login_fiscal_controller import LoginFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def login_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return LoginFiscalController(
        login_fiscal_case=LoginFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        create_refresh_token_fiscal=CreateRefreshTokenFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_refresh_token_fiscal=UpdateRefreshTokenFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 