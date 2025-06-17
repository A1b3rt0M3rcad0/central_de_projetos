from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.repository.types_repository import TypesRepository
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.find_all_bairro import FindAllBairro
from src.data.use_cases.find_all_empresas import FindAllEmpresas
from src.data.use_cases.find_all_fiscal import FindAllFiscal
from src.data.use_cases.find_all_types import FindAllTypes
from src.data.use_cases.find_all_user_by_role import FindAllUserByRole
from src.presentation.controllers.find_all_associations_possibility_from_project_controller import FindAllAssociationsPossiblityFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_associations_possibility_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllAssociationsPossiblityFromProjectController(
        find_all_bairro=FindAllBairro(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_all_empresas=FindAllEmpresas(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_all_fiscal=FindAllFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),

        find_all_types=FindAllTypes(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_all_user_by_role=FindAllUserByRole(
            user_project_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle