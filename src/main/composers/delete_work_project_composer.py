from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.presentation.controllers.delete_work_project_controller import DeleteWorkProjectController
from src.data.use_cases.delete_work_project import DeleteWorkProject
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_work_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteWorkProjectController(
        delete_work_project_case=DeleteWorkProject(
            work_project_repository=WorkProjectRepository(db_connection_handler_factory()),
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(raven_connection_handler_factory())
        )
    ).handle 