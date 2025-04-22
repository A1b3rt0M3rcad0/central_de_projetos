from src.domain.value_objects.monetary_value import MonetaryValue
from abc import ABC, abstractmethod

class IUpdateProjectVerba(ABC):

    @abstractmethod
    def update(self, project_id:int, verba_disponivel:MonetaryValue) -> None:
        """
        Atualiza o valor da verba disponível de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            verba_disponivel: O novo valor da verba disponível para o projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao tentar atualizar a verba disponível no banco de dados.
        """