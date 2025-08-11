from src.infra.raven.config.connection.data_connection import DataConnection
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.delete_document import DeleteDocument
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler as RelationalDBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
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
        ),
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=RelationalDBConnectionHandler(
                    connection=StringConnection()
                )
            )
        )
    ).handle