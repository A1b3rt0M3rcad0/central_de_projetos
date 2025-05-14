from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_project_by_status import FindProjectByStatus
from src.presentation.controllers.find_project_by_status_controller import FindProjectByStatusController


def find_project_by_status_composer():
    return FindProjectByStatusController(
        find_project_by_status_case=FindProjectByStatus(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle