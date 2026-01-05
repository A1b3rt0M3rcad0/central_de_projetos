"""Get Gantt Data Composer"""
#pylint:disable=all
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.get_gantt_data_controller import GetGanttDataController
from src.data.use_cases.get_gantt_data import GetGanttData
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.infra.relational.repository.eap_dependency_repository import EAPDependencyRepository
from src.main.config.database.db_connection_handler_factory import (
    db_connection_handler_factory
)


def get_gantt_data_composer() -> Callable[[HttpRequest], HttpResponse]:
    """
    Composer para criar o controller de busca de dados do Gantt
    
    Returns:
        Callable que recebe HttpRequest e retorna HttpResponse
    """
    # Criar repositórios
    db_connection = db_connection_handler_factory()
    eap_item_repository = EAPItemRepository(db_connection)
    eap_repository = EAPRepository(db_connection, eap_item_repository)
    project_repository = ProjectRepository(db_connection)
    dependency_repository = EAPDependencyRepository(db_connection)
    
    # Criar use case
    use_case = GetGanttData(
        project_repository=project_repository,
        eap_repository=eap_repository,
        dependency_repository=dependency_repository
    )
    
    # Criar controller
    controller = GetGanttDataController(get_gantt_data_case=use_case)
    
    return controller.handle

