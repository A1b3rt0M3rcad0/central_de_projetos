from abc import ABC, abstractmethod
from datetime import datetime

class IUpdateProjectExpectedCompletionDate(ABC):

    @abstractmethod
    def update(self, project_id:int, expected_completion_date:datetime) -> None:
        """
        Atualiza a data de conclusão esperada de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            expected_completion_date: A nova data de conclusão esperada do projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao atualizar a data de conclusão esperada do projeto no banco de dados.
            InvalidExpectedCompletionDateError (400): Caso a data de conclusão esperada fornecida seja anterior à data de início do projeto.
        """