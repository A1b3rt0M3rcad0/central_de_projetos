from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.get_fiscal_document_controller import GetFiscalDocumentController
from src.data.use_cases.get_fiscal_document import GetFiscalDocument
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler

def get_fiscal_document_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_connection_handler=DBConnectionHandler(
        data_connection=DataConnection()
    )
    repository = ProjectDocumentFiscalRepository(db_connection_handler)
    use_case = GetFiscalDocument(repository)
    controller = GetFiscalDocumentController(use_case)
    return controller.handle 