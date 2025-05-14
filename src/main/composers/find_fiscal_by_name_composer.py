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