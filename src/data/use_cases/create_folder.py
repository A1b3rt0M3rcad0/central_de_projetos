from src.domain.use_cases.i_create_folder import ICreateFolder
from src.data.interface.i_folder_repository import IFolderRepository

class CreateFolder(ICreateFolder):
    
    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def create(self, name: str) -> None:
        try:
            self.__folder_repository.insert(
                name=name
            )
        except Exception as e:
            raise e from e

