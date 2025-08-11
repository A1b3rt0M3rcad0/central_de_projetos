from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.data.use_cases.get_work_project_by_fiscal import GetWorkProjectByFiscal
from src.presentation.controllers.get_work_project_by_fiscal_mobile_controller import GetWorkProjectByFiscalMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_work_project_by_fiscal_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectByFiscalMobileController(
        get_work_project_by_fiscal_case=GetWorkProjectByFiscal(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 