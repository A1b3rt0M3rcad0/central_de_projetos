from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class IUpdateUserCPF(ABC):

    @abstractmethod
    def update(self, cpf:CPF) -> None:
        """
        Atualiza o CPF de um usuário no banco de dados.

        Parâmetros:
            cpf: O novo CPF a ser atribuído ao usuário.

        Levanta:
            CpfAlreadyExistsError (400): Caso o CPF fornecido já exista no sistema.
            InvalidCpfError (400): Caso o CPF fornecido tenha um formato incorreto.
            InternalServerError (500): Caso ocorra um erro inesperado durante a atualização do CPF.
        """