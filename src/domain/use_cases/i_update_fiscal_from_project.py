from abc import ABC, abstractmethod

class IUpdateFiscalFromProject(ABC):

    @abstractmethod
    def update(self, project_id:int, fiscal_id:int, new_fiscal_id:int) -> None:
        '''
        Realiza a troca do fiscal de um projeto

        Parãmetros:
            project_id: ID do projeto
            fiscal_id: ID do fiscal
            new_fiscal_id: ID id do novo fiscal
        Levanta:
            ErrorOnUpdateFiscalFromProject: caso haja qualquer erro relacionado ao update do fiscal do projeto
        '''