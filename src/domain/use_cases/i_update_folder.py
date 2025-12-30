from abc import ABC, abstractmethod

class IUpdateFolder(ABC):

    @abstractmethod
    def update(self, folder_id: int, new_name: str) -> None:
        '''
        Atualiza o nome de uma pasta existente

        Parâmetros:
            folder_id: id da pasta
            new_name: novo nome da pasta
        Levanta:
            FolderNotExists: caso não encontre a pasta
            FolderAlreadyExists: caso o novo nome já exista
        '''

