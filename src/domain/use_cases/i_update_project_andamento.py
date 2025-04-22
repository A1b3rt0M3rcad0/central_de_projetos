from abc import ABC, abstractmethod

class IUpdateProjectAndamento(ABC):

    @abstractmethod
    def update(self, project_id:int, andamento_do_projeto:str) -> None:
        """
        Atualiza o andamento de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            andamento_do_projeto: O novo valor para o andamento do projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao atualizar o andamento do projeto no banco de dados.
        """