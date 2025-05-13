from src.presentation.controllers.create_project_bairro_controller import CreateProjectBairroController
from src.data.use_cases.create_project_bairro import CreateProjectBairro
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.find_bairro_by_id import FindBairrobyId
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from typing import Callable

def create_project_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectBairroController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(db_connection_handler_factory())
        ),
        create_project_bairro_case=CreateProjectBairro(
            project_bairro_repository=ProjectBairroRepository(db_connection_handler_factory())
        ),
        find_bairro_by_id=FindBairrobyId(
            bairro_repository=BairroRepository(db_connection_handler_factory())
        )
    ).handle