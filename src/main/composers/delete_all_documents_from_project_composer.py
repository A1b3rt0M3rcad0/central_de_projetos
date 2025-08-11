from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.delete_all_documents_from_project import DeleteAllDocumentsFromProject
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.delete_all_documents_from_project_controller import DeleteAllDocumentsFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_all_documents_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteAllDocumentsFromProjectController(
        delete_all_documents_from_project_case=DeleteAllDocumentsFromProject(
            project_document_repository=ProjectDocumentRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        ),
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle