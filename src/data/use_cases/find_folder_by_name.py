from src.domain.use_cases.i_find_folder_by_name import IFindFolderByName
from src.domain.entities.folder import FolderEntity
from src.data.interface.i_folder_repository import IFolderRepository
from typing import Optional

class FindFolderByName(IFindFolderByName):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def find(self, name: str) -> Optional[FolderEntity]:
        try:
            result = self.__folder_repository.find_by_name(
                name=name
            )
            return result
        except Exception as e:
            raise e from e

