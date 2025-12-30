from abc import ABC, abstractmethod

class IDeleteAllProjectsFromFolder(ABC):

    @abstractmethod
    def delete(self, folder_id: int) -> None:
        '''
        Remove todas as associações de projetos de uma pasta

        Parâmetros:
            folder_id: ID da pasta
        '''

