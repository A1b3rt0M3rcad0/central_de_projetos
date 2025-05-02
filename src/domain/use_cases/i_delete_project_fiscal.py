from abc import ABC, abstractmethod

class IDeleteProjectFiscal(ABC):

    @abstractmethod
    def delete(self, project_id:int, fiscal_id:int) -> None:
        '''
        Deleta uma associação de projeto e fiscal

        Parâmetros:
            project_id: ID do projeto
            fiscal_id: ID do fiscal
        Levanta:
            ErrorOnDeleteProjectFiscal: Caso ocorra qualquer erro relacionado a deleção de um ProjectFiscal
        '''