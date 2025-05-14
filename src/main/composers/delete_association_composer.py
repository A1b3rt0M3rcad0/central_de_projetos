from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.data.use_cases.delete_association import DeleteAssociation
from src.presentation.controllers.delete_association_controller import DeleteAssociationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_association_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteAssociationController(
        delete_association_case=DeleteAssociation(
            user_project_repository=UserProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle