from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.find_all_folder import FindAllFolder
from src.presentation.controllers.find_all_folder_controller import FindAllFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFolderController(
        find_all_folder_case=FindAllFolder(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

