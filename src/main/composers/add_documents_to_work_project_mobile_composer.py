from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.data.use_cases.save_fiscal_document import SaveFiscalDocument
from src.data.use_cases.update_work_project_documents import UpdateWorkProjectDocuments
from src.data.use_cases.get_work_project import GetWorkProject
from src.data.use_cases.verify_fiscal_work_project_association import VerifyFiscalWorkProjectAssociation
from src.presentation.controllers.add_documents_to_work_project_mobile_controller import AddDocumentsToWorkProjectMobileController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def add_documents_to_work_project_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    return AddDocumentsToWorkProjectMobileController(
        save_fiscal_document_case=SaveFiscalDocument(
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        ),
        update_work_project_documents_case=UpdateWorkProjectDocuments(
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
        )
    ).handle 