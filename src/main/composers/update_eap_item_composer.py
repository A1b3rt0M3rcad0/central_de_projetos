from typing import Callable

from src.data.use_cases.update_eap_item import UpdateEAPItem
from src.data.use_cases.find_eap_item import FindEAPItem
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.presentation.controllers.update_eap_item_controller import UpdateEAPItemController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def update_eap_item_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para atualização de item da EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    
    # Casos de uso
    find_eap_item_case = FindEAPItem(eap_item_repository)
    update_eap_item_case = UpdateEAPItem(eap_item_repository, find_eap_item_case)
    
    # Controller
    controller = UpdateEAPItemController(update_eap_item_case)
    
    return controller.handle

