from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class ILogin(ABC):

    @abstractmethod
    def check(self, cpf:CPF, password:Password) -> str:
        """
        Verifica as credenciais de login de um usuário.

        Parâmetros:
            cpf: CPF do usuário que está tentando fazer login.
            password: Senha fornecida pelo usuário.

        Retorno:
            Um JWT (JSON Web Token) se as credenciais forem válidas.
            Payload Antes do Encode: 
            {
                'cpf': numero_do_cpf (int),
                'role': role_do_usuario (str),
                'exp': data_de_expiração (datetime)
            }

        Levanta:
            UserNotFoundError (404): Caso o CPF não seja encontrado ou a senha não seja válida.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """