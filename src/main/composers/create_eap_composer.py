from typing import Callable

from src.data.use_cases.create_eap import CreateEAP
from src.data.use_cases.find_eap import FindEAP
from src.data.use_cases.find_eap_item import FindEAPItem
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.presentation.controllers.create_eap_controller import CreateEAPController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def create_eap_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para criação de EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    eap_repository = EAPRepository(db_connection_handler_factory(), eap_item_repository)
    
    # Casos de uso
    find_eap_case = FindEAP(eap_repository)
    create_eap_case = CreateEAP(eap_repository, eap_item_repository, find_eap_case)
    
    # Controller
    controller = CreateEAPController(create_eap_case)
    
    return controller.handle