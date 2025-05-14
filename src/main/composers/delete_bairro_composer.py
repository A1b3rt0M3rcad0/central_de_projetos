from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.delete_bairro import DeleteBairro
from src.presentation.controllers.delete_bairro_controller import DeleteBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteBairroController(
        delete_bairro_case=DeleteBairro(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle