from abc import ABC, abstractmethod

class IUpdateFiscalStatus(ABC):

    @abstractmethod
    def update(self, fiscal_id: int, is_active: int) -> None:
        """
        Atualiza o status (ativo/inativo) de um fiscal.

        Parâmetros:
            fiscal_id: ID do fiscal a ser atualizado.
            is_active: Status do fiscal (1 = ativo, 0 = inativo).

        Retorno:
            None

        Levanta:
            FiscalNotFoundError (404): Caso o fiscal não seja encontrado.
            InvalidParameterError (422): Caso o valor de is_active seja inválido.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """

