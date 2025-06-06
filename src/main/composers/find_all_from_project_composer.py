from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.raven.repositories.project_document_repository import ProjectDocumentRepository
from src.data.use_cases.find_all_from_project import FindAllFromProject
from src.data.use_cases.get_document_names import GetDocumentNames
from src.presentation.controllers.find_all_from_project_controller import FindAllFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFromProjectController(
        find_all_from_project_case=FindAllFromProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        get_document_names_case=GetDocumentNames(
            project_documents_repository=ProjectDocumentRepository(
                db_connection_handler=raven_connection_handler_factory()
            )
        ) 
    ).handle