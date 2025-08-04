from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.delete_all_fiscal_documents_from_project_controller import DeleteAllFiscalDocumentsFromProjectController
from src.data.use_cases.delete_all_fiscal_documents_from_project import DeleteAllFiscalDocumentsFromProject
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler

def delete_all_fiscal_documents_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_connection_handler=DBConnectionHandler(
        data_connection=DataConnection()
    )
    repository = ProjectDocumentFiscalRepository(db_connection_handler)
    use_case = DeleteAllFiscalDocumentsFromProject(repository)
    controller = DeleteAllFiscalDocumentsFromProjectController(use_case)
    return controller.handle 