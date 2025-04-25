from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectEndDate(ABC):

    @abstractmethod
    def update(self, project_id:int, end_date:datetime) -> None:
        """
        Atualiza a data de término de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            end_date: A nova data de término do projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao atualizar a data de término do projeto no banco de dados.
            InvalidEndDateError (400): Caso a data de término fornecida seja anterior à data de início do projeto.
        """