from src.presentation.controllers.delete_project_controller import DeleteProjectController
from src.data.use_cases.delete_project import DeleteProject
from src.data.use_cases.delete_all_history_project_from_project import DeleteAllHistoryProjectFromProject
from src.data.use_cases.delete_association_user_from_project import DeleteAssociationUserFromProject
from src.data.use_cases.delete_bairro_from_project import DeleteBairroFromProject
from src.data.use_cases.delete_empresa_from_project import DeleteEmpresaFromProject
from src.data.use_cases.delete_fiscal_from_project import DeleteFiscalFromProject
from src.data.use_cases.delete_type_from_project import DeleteTypeFromProject
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_handler = db_connection_handler_factory()

    return DeleteProjectController(
        delete_project_case=DeleteProject(
            project_repository=ProjectRepository(db_connection_handler=db_handler)
        ),
        delete_all_history_project_from_project_case=DeleteAllHistoryProjectFromProject(
            history_project_repository=HistoryProjectRepository(db_connection_handler=db_handler)
        ),
        delete_association_user_from_project_case=DeleteAssociationUserFromProject(
            user_project_repository=UserProjectRepository(db_connection_handler=db_handler)
        ),
        delete_bairro_from_project_case=DeleteBairroFromProject(
            project_bairro_repository=ProjectBairroRepository(db_connection_handler=db_handler)
        ),
        delete_empresa_from_project_case=DeleteEmpresaFromProject(
            project_empresa_repository=ProjectEmpresaRepository(db_connection_handler=db_handler)
        ),
        delete_fiscal_from_project_case=DeleteFiscalFromProject(
            project_fiscal_repository=ProjectFiscalRepository(db_connection_handler=db_handler)
        ),
        delete_type_from_project_case=DeleteTypeFromProject(
            project_type_repository=ProjectTypeRepository(db_connection_handler=db_handler)
        )
    ).handle