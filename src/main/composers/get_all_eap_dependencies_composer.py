"""Composer para buscar TODAS as dependências de uma EAP de uma vez"""
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.controllers.get_all_eap_dependencies_controller import (
    GetAllEAPDependenciesController
)
from src.data.use_cases.get_all_eap_dependencies import GetAllEAPDependencies
from src.infra.relational.repository.eap_dependency_repository import EAPDependencyRepository
from src.infra.relational.repository.eap_item_repository import EAPItemRepository
from src.infra.relational.repository.eap_repository import EAPRepository
from src.main.config.database.db_connection_handler_factory import (
    db_connection_handler_factory
)


def get_all_eap_dependencies_composer() -> Callable[[HttpRequest], HttpResponse]:
    """
    Composer para buscar TODAS as dependências de todos os itens de uma EAP de uma vez
    
    Returns:
        Callable: Handler do controller
    """
    db_handler = db_connection_handler_factory()
    eap_item_repository = EAPItemRepository(db_handler)
    
    return GetAllEAPDependenciesController(
        use_case=GetAllEAPDependencies(
            dependency_repository=EAPDependencyRepository(db_handler),
            eap_repository=EAPRepository(db_handler, eap_item_repository)
        )
    ).handle

