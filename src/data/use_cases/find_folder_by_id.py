from src.domain.use_cases.i_find_folder_by_id import IFindFolderById
from src.domain.entities.folder import FolderEntity
from src.data.interface.i_folder_repository import IFolderRepository

class FindFolderById(IFindFolderById):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def find(self, folder_id: int) -> FolderEntity:
        try:
            result = self.__folder_repository.find_by_id(
                folder_id=folder_id
            )
            return result
        except Exception as e:
            raise e from e

