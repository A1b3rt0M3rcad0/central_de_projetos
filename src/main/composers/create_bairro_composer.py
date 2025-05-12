from src.data.use_cases.create_bairro import CreateBairro
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.create_bairro_controller import CreateBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateBairroController(
        CreateBairro(
            BairroRepository(
                db_connection_handler_factory()
            )
        )
    ).handle