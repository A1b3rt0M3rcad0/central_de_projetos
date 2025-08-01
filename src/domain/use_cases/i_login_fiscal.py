from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from abc import ABC, abstractmethod

class ILoginFiscal(ABC):

    @abstractmethod
    def check(self, email:Email, password:Password) -> str:
        """
        Verifica as credenciais de login de um fiscal.

        Parâmetros:
            email: Email do fiscal que está tentando fazer login.
            password: Senha fornecida pelo fiscal.

        Retorno:
            Um JWT (JSON Web Token) se as credenciais forem válidas.
            Payload Antes do Encode: 
            {
                'email': email_do_fiscal (str),
                'role': 'fiscal' (str),
                'exp': data_de_expiração (datetime)
            }

        Levanta:
            FiscalNotFoundError (404): Caso o email não seja encontrado ou a senha não seja válida.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """ 