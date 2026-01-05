from src.domain.use_cases.i_delete_folder import IDeleteFolder
from src.data.interface.i_folder_repository import IFolderRepository

class DeleteFolder(IDeleteFolder):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def delete(self, folder_id: int) -> None:
        try:
            self.__folder_repository.delete(
                folder_id=folder_id
            )
        except Exception as e:
            raise e from e

