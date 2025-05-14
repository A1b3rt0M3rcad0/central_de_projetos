from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.types_repository import TypesRepository
from src.data.use_cases.find_type_by_exact_name import FindTypebyExactName
from src.presentation.controllers.find_type_by_exact_name_controller import FindTypeByExactNameController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_type_by_exact_name_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindTypeByExactNameController(
        find_type_by_exact_name_case=FindTypebyExactName(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle