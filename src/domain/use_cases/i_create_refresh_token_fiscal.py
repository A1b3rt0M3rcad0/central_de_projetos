from src.domain.value_objects.email import Email
from abc import ABC, abstractmethod

class ICreateRefreshTokenFiscal(ABC):

    @abstractmethod
    def create(self, email: Email) -> None:
        """
        Cria um refresh token para um fiscal.

        Parâmetros:
            email: Email do fiscal para o qual criar o refresh token.

        Levanta:
            InternalServerError (500): Para qualquer erro durante a operação.
        """
    
    @abstractmethod
    def generate_token(self, email: Email) -> str:
        """
        Gera um refresh token para um fiscal.

        Parâmetros:
            email: Email do fiscal para o qual gerar o refresh token.

        Retorno:
            Um JWT (JSON Web Token) que serve como refresh token.
            Payload Antes do Encode: 
            {
                'email': email_do_fiscal (str),
                'exp': data_de_expiração (datetime)
            }
        """ 