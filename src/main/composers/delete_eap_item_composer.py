from typing import Callable
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.find_eap_item import FindEAPItem
from src.data.use_cases.find_eap import FindEAP
from src.data.use_cases.delete_eap_item import DeleteEAPItem
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.delete_eap_item_controller import DeleteEAPItemController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def delete_eap_item_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para exclusão de item da EAP"""
    
    # Repositórios
    db_handler = db_connection_handler_factory()
    eap_item_repository = EAPItemRepository(db_handler)
    eap_repository = EAPRepository(db_handler, eap_item_repository)
    history_repository = HistoryProjectRepository(db_handler)
    
    # Use cases
    find_eap_item_case = FindEAPItem(eap_item_repository)
    find_eap_case = FindEAP(eap_repository)
    delete_eap_item_case = DeleteEAPItem(eap_item_repository, find_eap_item_case)
    create_history_case = CreateHistoryProject(history_repository)
    
    # Controller
    controller = DeleteEAPItemController(delete_eap_item_case, create_history_case, find_eap_item_case, find_eap_case)
    
    return controller.handle
