from typing import Callable
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.data.use_cases.find_eap_item import FindEAPItem
from src.data.use_cases.delete_eap_item import DeleteEAPItem
from src.presentation.controllers.delete_eap_item_controller import DeleteEAPItemController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def delete_eap_item_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para exclusão de item da EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    
    # Use cases
    find_eap_item_case = FindEAPItem(eap_item_repository)
    delete_eap_item_case = DeleteEAPItem(eap_item_repository, find_eap_item_case)
    
    # Controller
    controller = DeleteEAPItemController(delete_eap_item_case)
    
    return controller.handle
