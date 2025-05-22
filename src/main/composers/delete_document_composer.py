from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.delete_document import DeleteDocument
from src.presentation.controllers.delete_document_controller import DeleteDocumentController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_document_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteDocumentController(
        delete_document_case=DeleteDocument(
            project_document_repository=ProjectDocumentRepository(
                db_connection_handler=DBConnectionHandler(
                    data_connection=DataConnection()
                )
            )
        )
    ).handle