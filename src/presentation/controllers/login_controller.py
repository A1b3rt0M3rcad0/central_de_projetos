from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_login import ILogin
from src.domain.use_cases.i_create_refresh_token import ICreateRefreshToken
from src.domain.use_cases.i_update_refresh_token import IUpdateRefreshToken
from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.errors.repository.already_exists_error.refresh_token_already_exists import RefreshTokenAlreadyExists

class LoginController(ControllerInterface):

    def __init__(self, 
                 login_case:ILogin, 
                 create_refresh_token:ICreateRefreshToken,
                 update_refresh_token:IUpdateRefreshToken
                 ) -> None:
        self.__login_case = login_case
        self.__create_refresh_token = create_refresh_token
        self.__update_refresh_token = update_refresh_token
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            password = Password(body['password'])
            token  = self.__login_case.check(
                cpf=cpf,
                password=password
            )
            self._create_refresh_token(cpf=cpf)
            return HttpResponse(
                status_code=200,
                body={
                    'token': token
                }
            )
        except Exception as e:
            raise e from e
    
    def _create_refresh_token(self, cpf:CPF) -> None:
        try:
            self.__create_refresh_token.create(
                cpf=cpf
            )
        except RefreshTokenAlreadyExists:
            self.__update_refresh_token.update(
                user_cpf=cpf,
                new_token=self.__create_refresh_token.generate_token(cpf)
            )