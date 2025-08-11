from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.data.use_cases.delete_fiscal_document_from_work_project import DeleteFiscalDocumentFromWorkProject
from src.data.use_cases.remove_document_from_work_project import RemoveDocumentFromWorkProject
from src.data.use_cases.get_work_project import GetWorkProject
from src.data.use_cases.verify_fiscal_work_project_association import VerifyFiscalWorkProjectAssociation
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.presentation.controllers.delete_document_from_work_project_mobile_controller import DeleteDocumentFromWorkProjectMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_document_from_work_project_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteDocumentFromWorkProjectMobileController(
        delete_fiscal_document_case=DeleteFiscalDocumentFromWorkProject(
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        ),
        remove_document_from_work_project_case=RemoveDocumentFromWorkProject(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        get_work_project_case=GetWorkProject(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        verify_fiscal_work_project_association_case=VerifyFiscalWorkProjectAssociation(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 