from abc import ABC, abstractmethod

class IUpdateProjectName(ABC):

    @abstractmethod
    def update(self, project_id:int, name:str) -> None:
        """
        Atualiza o nome de um projeto no banco de dados, identificando o projeto pelo ID.

        Parâmetros:
            project_id: O ID do projeto a ser atualizado.
            name: O novo nome a ser atribuído ao projeto.

        Levanta:
            InternalServerError (500): Caso ocorra um erro ao tentar atualizar o nome do projeto no banco de dados.
        """