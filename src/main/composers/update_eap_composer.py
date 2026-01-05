from typing import Callable

from src.data.use_cases.update_eap import UpdateEAP
from src.data.use_cases.find_eap import FindEAP
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.presentation.controllers.update_eap_controller import UpdateEAPController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def update_eap_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para atualização de EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    eap_repository = EAPRepository(db_connection_handler_factory(), eap_item_repository)
    
    # Casos de uso
    find_eap_case = FindEAP(eap_repository)
    update_eap_case = UpdateEAP(eap_repository, find_eap_case)
    
    # Controller
    controller = UpdateEAPController(update_eap_case)
    
    return controller.handle