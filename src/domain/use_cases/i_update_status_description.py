from abc import ABC, abstractmethod

class IUpdateStatusDescription(ABC):

    @abstractmethod
    def update(self, description:str) -> None:
        """
        Atualiza a descrição de um status.

        Parâmetros:
            description: A nova descrição para o status.

        Levanta:
            StatusDescriptionError (400): Caso a descrição fornecida já exista.
            InternalServerError (500): Caso ocorra outro erro durante o processo de atualização da descrição.
        """
