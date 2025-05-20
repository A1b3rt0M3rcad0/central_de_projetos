from abc import ABC, abstractmethod

class IDeleteProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Deleta um projeto

        Parâmetros:
            project_id: ID do projeto
        Levanta:
            ErrorOnDeleteProject: Caso ocorra qualquer erro relacionado a deleção de um ProjectFiscal
        '''