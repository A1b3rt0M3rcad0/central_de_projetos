from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.find_all_folders_with_pagination import FindAllFoldersWithPagination
from src.presentation.controllers.find_all_folders_with_pagination_controller import FindAllFoldersWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_folders_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_handler = db_connection_handler_factory()
    folder_repository = FolderRepository(db_connection_handler=db_handler)
    return FindAllFoldersWithPaginationController(
        find_all_folders_with_pagination_case=FindAllFoldersWithPagination(
            folder_repository=folder_repository
        ),
        folder_repository=folder_repository
    ).handle

