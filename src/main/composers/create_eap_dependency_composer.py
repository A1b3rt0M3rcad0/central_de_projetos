"""Composer para criar dependência entre itens da EAP"""
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.create_eap_dependency_controller import CreateEAPDependencyController
from src.data.use_cases.create_eap_dependency import CreateEAPDependency
from src.infra.relational.repository.eap_dependency_repository import EAPDependencyRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory


def create_eap_dependency_composer() -> Callable[[HttpRequest], HttpResponse]:
    """
    Composer para criar dependência entre itens da EAP
    
    Returns:
        Callable: Handler do controller
    """
    return CreateEAPDependencyController(
        use_case=CreateEAPDependency(
            dependency_repository=EAPDependencyRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            eap_item_repository=EAPItemRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

