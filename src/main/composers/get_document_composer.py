from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.get_document import GetDocument
from src.presentation.controllers.get_document_controller import GetDocumentController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_document_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetDocumentController(
        get_document_case=GetDocument(
            project_document_repository=ProjectDocumentRepository(
                db_connection_handler=DBConnectionHandler(
                    data_connection=DataConnection()
                )
            )
        )
    ).handle