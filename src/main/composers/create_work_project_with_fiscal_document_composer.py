from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.create_work_project_with_fiscal_document_controller import CreateWorkProjectWithFiscalDocumentController
from src.data.use_cases.insert_work_project import InsertWorkProject
from src.data.use_cases.save_fiscal_document import SaveFiscalDocument
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler as RavenDBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection as RavenDataConnection
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository

def create_work_project_with_fiscal_document_composer() -> Callable[[HttpRequest], HttpResponse]:
    # Configuração para work project (relational database)
    db_connection_handler = DBConnectionHandler(
        connection=StringConnection()
    )
    work_project_repository = WorkProjectRepository(db_connection_handler)
    insert_work_project_use_case = InsertWorkProject(work_project_repository)
    
    # Configuração para fiscal documents (Raven database)
    raven_db_connection_handler = RavenDBConnectionHandler(
        data_connection=RavenDataConnection()
    )
    fiscal_document_repository = ProjectDocumentFiscalRepository(raven_db_connection_handler)
    save_fiscal_document_use_case = SaveFiscalDocument(fiscal_document_repository)
    
    # Configuração para history project
    history_project_repository = HistoryProjectRepository(db_connection_handler)
    create_history_project_use_case = CreateHistoryProject(history_project_repository)
    
    # Controller
    controller = CreateWorkProjectWithFiscalDocumentController(
        insert_work_project_case=insert_work_project_use_case,
        save_fiscal_document_case=save_fiscal_document_use_case,
        create_history_project_case=create_history_project_use_case
    )
    return controller.handle 