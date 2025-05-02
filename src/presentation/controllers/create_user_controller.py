from src.domain.use_cases.i_create_user import ICreateUser
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.roles import Role
from src.domain.value_objects.password import Password

class CreateUserController(ControllerInterface):

    def __init__(self, create_user_case:ICreateUser) -> None:
        self.__create_user_case = create_user_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            email = Email(body['email'])
            role = Role(body['role'])
            password = Password(body['password'])
            self.__create_user_case.create(
                cpf=cpf,
                email=email,
                role=role,
                password=password
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'User created'
                }
            )
        except Exception as e:
            raise e from e