from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.data.use_cases.get_work_project_document import GetWorkProjectDocument
from src.data.use_cases.get_work_project import GetWorkProject
from src.data.use_cases.find_project_fiscal import FindProjectFiscal
from src.presentation.controllers.get_work_project_document_mobile_controller import GetWorkProjectDocumentMobileController

def get_work_project_document_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectDocumentMobileController(
        get_work_project_document_case=GetWorkProjectDocument(
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        ),
        get_work_project_case=GetWorkProject(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_project_fiscal_case=FindProjectFiscal(
            project_fiscal_repository=ProjectFiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
    ).handle 