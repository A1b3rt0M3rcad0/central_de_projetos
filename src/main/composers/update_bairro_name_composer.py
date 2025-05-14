from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.update_bairro_name import UpdateBairroName
from src.presentation.controllers.update_bairro_name_controller import UpdateBairroNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_bairro_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateBairroNameController(
        update_bairro_name_case=UpdateBairroName(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle