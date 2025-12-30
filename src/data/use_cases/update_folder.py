from src.domain.use_cases.i_update_folder import IUpdateFolder
from src.data.interface.i_folder_repository import IFolderRepository

class UpdateFolder(IUpdateFolder):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def update(self, folder_id: int, new_name: str) -> None:
        try:
            self.__folder_repository.update(
                folder_id=folder_id,
                new_name=new_name
            )
        except Exception as e:
            raise e from e

