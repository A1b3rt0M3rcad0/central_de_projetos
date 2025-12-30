from src.data.use_cases.create_folder import CreateFolder
from src.infra.relational.repository.folder_repository import FolderRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.create_folder_controller import CreateFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateFolderController(
        CreateFolder(
            FolderRepository(
                db_connection_handler_factory()
            )
        )
    ).handle

