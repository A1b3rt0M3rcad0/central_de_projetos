from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.infra.relational.repository.user_repository import UserRepository
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.data.use_cases.update_association_from_project import UpdateAssociationFromProject
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.update_association_from_project_controller import UpdateAssociationFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_association_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateAssociationFromProjectController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_association_from_project_case=UpdateAssociationFromProject(
            user_project_repository=UserProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle