from abc import ABC, abstractmethod

class IDeleteAllDocumentsFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Deleta todos os projetos do ravendb
        '''