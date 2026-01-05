from typing import Callable

from src.data.use_cases.find_eap import FindEAP
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.presentation.controllers.find_eap_controller import FindEAPController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def find_eap_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para busca de EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    eap_repository = EAPRepository(db_connection_handler_factory(), eap_item_repository)
    
    # Casos de uso
    find_eap_case = FindEAP(eap_repository)
    
    # Controller
    controller = FindEAPController(find_eap_case)
    
    return controller.handle