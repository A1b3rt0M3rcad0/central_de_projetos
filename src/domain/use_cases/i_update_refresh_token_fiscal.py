from src.domain.value_objects.email import Email
from abc import ABC, abstractmethod

class IUpdateRefreshTokenFiscal(ABC):

    @abstractmethod
    def update(self, fiscal_email: Email, new_token: str) -> None:
        """
        Atualiza o refresh token de um fiscal.

        Parâmetros:
            fiscal_email: Email do fiscal para o qual atualizar o refresh token.
            new_token: Novo token de refresh.

        Levanta:
            InternalServerError (500): Para qualquer erro durante a operação.
        """ 