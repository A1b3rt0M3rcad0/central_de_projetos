from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.update_user_name import UpdateUserName
from src.data.use_cases.update_user_email import UpdateUserEmail
from src.data.use_cases.update_user_password import UpdateUserPassword
from src.data.use_cases.find_user import FindUser
from src.presentation.controllers.update_user_personal_data_controller import UpdateUserPersonalDataController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_user_personal_data_composer() -> Callable[[HttpRequest], HttpResponse]:
    """
    Composer para o endpoint de atualização de dados pessoais do usuário.
    """
    db_connection = db_connection_handler_factory()
    user_repository = UserRepository(db_connection_handler=db_connection)
    
    return UpdateUserPersonalDataController(
        update_user_name_case=UpdateUserName(user_repository=user_repository),
        update_user_email_case=UpdateUserEmail(user_repository=user_repository),
        update_user_password_case=UpdateUserPassword(user_repository=user_repository),
        find_user_case=FindUser(user_repository=user_repository)
    ).handle

