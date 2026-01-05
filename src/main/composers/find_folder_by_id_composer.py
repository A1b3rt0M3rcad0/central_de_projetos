from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.find_folder_by_id import FindFolderById
from src.presentation.controllers.find_folder_by_id_controller import FindFolderByIdController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_folder_by_id_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindFolderByIdController(
        find_folder_by_id_case=FindFolderById(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

