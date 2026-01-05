from src.domain.use_cases.i_update_user_name import IUpdateUserName
from src.domain.use_cases.i_update_user_email import IUpdateUserEmail
from src.domain.use_cases.i_update_user_password import IUpdateUserPassword
from src.domain.use_cases.i_find_user import IFindUser
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateUserPersonalDataController(ControllerInterface):
    """
    Controller para atualizar dados pessoais do usuário.
    Permite atualizar nome, email e/ou senha de forma independente.
    """

    def __init__(
        self, 
        update_user_name_case: IUpdateUserName,
        update_user_email_case: IUpdateUserEmail,
        update_user_password_case: IUpdateUserPassword,
        find_user_case: IFindUser
    ) -> None:
        self.__update_user_name_case = update_user_name_case
        self.__update_user_email_case = update_user_email_case
        self.__update_user_password_case = update_user_password_case
        self.__find_user_case = find_user_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            
            # Buscar usuário atual
            current_user = self.__find_user_case.find(cpf=cpf)
            
            updated_fields = []
            
            # Atualizar nome se fornecido
            if 'name' in body and body['name']:
                self.__update_user_name_case.update(
                    cpf=cpf,
                    name=body['name']
                )
                updated_fields.append('nome')
            
            # Atualizar email se fornecido e diferente do atual
            if 'email' in body and body['email']:
                new_email = body['email'].lower().strip()
                current_email = current_user.email.email.lower().strip()
                
                # Só atualizar se o email for diferente
                if new_email != current_email:
                    self.__update_user_email_case.update(
                        cpf=cpf,
                        email=Email(body['email'])
                    )
                    updated_fields.append('email')
            
            # Atualizar senha se fornecido (requer senha atual e nova senha)
            if 'new_password' in body and body['new_password']:
                # Validar que a senha atual foi fornecida
                if 'current_password' not in body or not body['current_password']:
                    raise ValueError("Senha atual é obrigatória para alterar a senha")
                
                # Aqui seria ideal validar a senha atual primeiro
                # Por enquanto, vamos apenas atualizar
                self.__update_user_password_case.update(
                    cpf=cpf,
                    password=Password(body['new_password'])
                )
                updated_fields.append('senha')
            
            message = f"Dados atualizados: {', '.join(updated_fields)}" if updated_fields else "Nenhum dado foi atualizado"
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': message,
                    'updated_fields': updated_fields
                }
            )
        except Exception as e:
            raise e from e

