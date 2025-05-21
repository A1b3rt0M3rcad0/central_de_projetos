from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.save_document import SaveDocument
from src.presentation.controllers.save_document_controller import SaveDocumentController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def save_document_composer() -> Callable[[HttpRequest], HttpResponse]:
    return SaveDocumentController(
        save_document_use_case=SaveDocument(
            project_document_repository=ProjectDocumentRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        )
    ).handle