from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.delete_folder import DeleteFolder
from src.presentation.controllers.delete_folder_controller import DeleteFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteFolderController(
        delete_folder_case=DeleteFolder(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

