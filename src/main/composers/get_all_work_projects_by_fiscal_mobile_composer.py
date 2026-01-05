from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_all_work_projects_by_fiscal_mobile_controller import GetAllWorkProjectsByFiscalMobileController
from src.data.use_cases.get_work_projects_by_fiscal_with_pagination import GetWorkProjectsByFiscalWithPagination
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


def get_all_work_projects_by_fiscal_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetAllWorkProjectsByFiscalMobileController(
        get_work_projects_by_fiscal_with_pagination_case=GetWorkProjectsByFiscalWithPagination(
            WorkProjectRepository(db_connection_handler_factory())
        )
    ).handle


