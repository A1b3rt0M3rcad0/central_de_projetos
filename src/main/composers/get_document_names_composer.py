from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.get_document_names import GetDocumentNames
from src.presentation.controllers.get_document_names_controller import GetDocumentNamesController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_document_names_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetDocumentNamesController(
        get_document_names_case=GetDocumentNames(
            project_documents_repository=(
                ProjectDocumentRepository(
                    db_connection_handler=DBConnectionHandler(
                        data_connection=DataConnection()
                    )
                )
            )
        )
    ).handle