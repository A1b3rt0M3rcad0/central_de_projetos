from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.find_bairro_by_name import FindBairroByName
from src.presentation.controllers.find_bairro_by_name_controller import FindBairrobyNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_bairr_by_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindBairrobyNameController(
        find_bairro_by_name_case=FindBairroByName(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle