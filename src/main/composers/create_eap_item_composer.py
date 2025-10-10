from typing import Callable

from src.data.use_cases.create_eap_item import CreateEAPItem
from src.data.use_cases.find_eap import FindEAP
from src.data.use_cases.find_eap_item import FindEAPItem
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.presentation.controllers.create_eap_item_controller import CreateEAPItemController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def create_eap_item_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para criação de item da EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    eap_repository = EAPRepository(db_connection_handler_factory(), eap_item_repository)
    
    # Casos de uso
    find_eap_case = FindEAP(eap_repository)
    find_eap_item_case = FindEAPItem(eap_item_repository)
    create_eap_item_case = CreateEAPItem(eap_item_repository, find_eap_case, find_eap_item_case)
    
    # Controller
    controller = CreateEAPItemController(create_eap_item_case)
    
    return controller.handle