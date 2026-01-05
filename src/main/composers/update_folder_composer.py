from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.update_folder import UpdateFolder
from src.presentation.controllers.update_folder_controller import UpdateFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateFolderController(
        update_folder_case=UpdateFolder(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

