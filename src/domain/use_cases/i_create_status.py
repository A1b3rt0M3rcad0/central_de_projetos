from abc import ABC, abstractmethod

class ICreateStatus(ABC):

    @abstractmethod
    def create(self, description:str) -> None:
        """
        Cria um novo status e o insere no banco de dados.

        Parâmetros:
            description: Descrição do status a ser criado.

        Levanta:
            InternalServerError (500): Se ocorrer qualquer erro durante a criação do status.
        """