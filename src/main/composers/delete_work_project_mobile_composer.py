from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.delete_work_project_mobile_controller import DeleteWorkProjectMobileController
from src.data.use_cases.delete_work_project_by_fiscal import DeleteWorkProjectByFiscal
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.infra.raven.config.connection.db_connection_handler import DBConnectionHandler as RavenDBConnectionHandler
from src.infra.raven.config.connection.data_connection import DataConnection as RavenDataConnection

def delete_work_project_mobile_composer() -> Callable[[HttpRequest], HttpResponse]:
    # Configuração para work project (relational database)
    db_connection_handler = DBConnectionHandler(
        connection=StringConnection()
    )
    work_project_repository = WorkProjectRepository(db_connection_handler)
    
    # Configuração para fiscal documents (Raven database)
    raven_db_connection_handler = RavenDBConnectionHandler(
        data_connection=RavenDataConnection()
    )
    fiscal_document_repository = ProjectDocumentFiscalRepository(raven_db_connection_handler)
    
    # Caso de uso para deletar work project por fiscal
    delete_work_project_by_fiscal_use_case = DeleteWorkProjectByFiscal(
        work_project_repository=work_project_repository,
        project_document_fiscal_repository=fiscal_document_repository
    )
    
    # Configuração para history project
    history_project_repository = HistoryProjectRepository(db_connection_handler)
    create_history_project_use_case = CreateHistoryProject(history_project_repository)
    
    # Controller
    controller = DeleteWorkProjectMobileController(
        delete_work_project_by_fiscal_case=delete_work_project_by_fiscal_use_case,
        create_history_project_case=create_history_project_use_case
    )
    return controller.handle 