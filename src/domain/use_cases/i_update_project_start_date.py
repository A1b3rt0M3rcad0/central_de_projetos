from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectStartDate(ABC):

    @abstractmethod
    def update(self, project_id:int, start_date:datetime) -> None:
        """
        Atualiza a data de início de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            start_date: A nova data de início a ser atribuída ao projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao tentar atualizar a data de início do projeto no banco de dados.
        """