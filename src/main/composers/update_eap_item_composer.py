from typing import Callable

from src.data.use_cases.update_eap_item import UpdateEAPItem
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.find_eap_item import FindEAPItem
from src.data.use_cases.find_eap import FindEAP
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.presentation.controllers.update_eap_item_controller import UpdateEAPItemController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def update_eap_item_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para atualização de item da EAP"""
    
    # Repositórios
    db_handler = db_connection_handler_factory()
    eap_item_repository = EAPItemRepository(db_handler)
    eap_repository = EAPRepository(db_handler, eap_item_repository)
    history_repository = HistoryProjectRepository(db_handler)
    
    # Casos de uso
    find_eap_item_case = FindEAPItem(eap_item_repository)
    find_eap_case = FindEAP(eap_repository)
    update_eap_item_case = UpdateEAPItem(eap_item_repository, find_eap_item_case)
    create_history_case = CreateHistoryProject(history_repository)
    
    # Controller
    controller = UpdateEAPItemController(update_eap_item_case, create_history_case, find_eap_case)
    
    return controller.handle

