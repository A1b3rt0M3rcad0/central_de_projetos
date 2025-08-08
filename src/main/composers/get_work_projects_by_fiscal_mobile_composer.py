from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_work_projects_by_fiscal_mobile_controller import GetWorkProjectsByFiscalMobileController
from src.data.use_cases.get_work_projects_by_fiscal_mobile import GetWorkProjectsByFiscalMobile
from src.data.use_cases.find_project_fiscal import FindProjectFiscal
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_work_projects_by_fiscal_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectsByFiscalMobileController(
        get_work_projects_by_fiscal_mobile_case=GetWorkProjectsByFiscalMobile(WorkProjectRepository(db_connection_handler_factory())),
        find_project_fiscal_case=FindProjectFiscal(ProjectFiscalRepository(db_connection_handler_factory()))
    ).handle 