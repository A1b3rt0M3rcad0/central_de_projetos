from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.count_bairros import CountBairros
from src.presentation.controllers.count_bairros_controller import CountBairrosController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def count_bairros_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CountBairrosController(
        count_bairros=CountBairros(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle