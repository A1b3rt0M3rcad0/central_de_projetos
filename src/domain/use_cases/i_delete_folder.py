from abc import ABC, abstractmethod

class IDeleteFolder(ABC):

    @abstractmethod
    def delete(self, folder_id: int) -> None:
        '''
        Deleta a pasta pelo id

        Parâmetros:
            folder_id: id da pasta
        Levanta:
            FolderNotExists: caso não encontre a pasta
            FolderHasRelatedChildren: caso a pasta tenha projetos associados
        '''

