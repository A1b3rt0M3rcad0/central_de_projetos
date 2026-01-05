from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.count_folders import CountFolders
from src.presentation.controllers.count_folders_controller import CountFoldersController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def count_folders_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CountFoldersController(
        count_folders=CountFolders(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

