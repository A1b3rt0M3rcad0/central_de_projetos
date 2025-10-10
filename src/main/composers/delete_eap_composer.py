from typing import Callable
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.eap_repository import EAPRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.data.use_cases.find_eap import FindEAP
from src.data.use_cases.delete_eap import DeleteEAP
from src.presentation.controllers.delete_eap_controller import DeleteEAPController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


def delete_eap_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Compositor para exclusão de EAP"""
    
    # Repositórios
    eap_item_repository = EAPItemRepository(db_connection_handler_factory())
    eap_repository = EAPRepository(db_connection_handler_factory(), eap_item_repository)
    
    # Use cases
    find_eap_case = FindEAP(eap_repository)
    delete_eap_case = DeleteEAP(eap_repository, find_eap_case)
    
    # Controller
    controller = DeleteEAPController(delete_eap_case)
    
    return controller.handle
