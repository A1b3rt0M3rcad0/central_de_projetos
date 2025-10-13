"""Composer para deletar dependência entre itens da EAP"""
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.delete_eap_dependency_controller import DeleteEAPDependencyController
from src.data.use_cases.delete_eap_dependency import DeleteEAPDependency
from src.infra.relational.repository.eap_dependency_repository import EAPDependencyRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory


def delete_eap_dependency_composer() -> Callable[[HttpRequest], HttpResponse]:
    """
    Composer para deletar dependência entre itens da EAP
    
    Returns:
        Callable: Handler do controller
    """
    return DeleteEAPDependencyController(
        use_case=DeleteEAPDependency(
            dependency_repository=EAPDependencyRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

