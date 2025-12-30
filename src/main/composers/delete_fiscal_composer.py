"""
Composer responsável por montar a cadeia de dependências para o endpoint de deleção de fiscal.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia todos os repositórios necessários
- Instancia o use case DeleteFiscal com todas as dependências
- Instancia o controller DeleteFiscalController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.main.config.database.raven_connection_handler_factory import raven_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.infra.raven.repositories.project_document_fiscal_repository import ProjectDocumentFiscalRepository
from src.data.use_cases.delete_fiscal import DeleteFiscal
from src.presentation.controllers.delete_fiscal_controller import DeleteFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_handler = db_connection_handler_factory()
    raven_handler = raven_connection_handler_factory()
    
    return DeleteFiscalController(
        delete_fiscal_case=DeleteFiscal(
            fiscal_repository=FiscalRepository(db_connection_handler=db_handler),
            project_fiscal_repository=ProjectFiscalRepository(db_connection_handler=db_handler),
            work_project_repository=WorkProjectRepository(db_connection_handler=db_handler),
            project_document_fiscal_repository=ProjectDocumentFiscalRepository(db_connection_handler=raven_handler)
        )
    ).handle