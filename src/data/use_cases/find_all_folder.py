from src.domain.use_cases.i_find_all_folder import IFindAllFolder
from src.domain.entities.folder import FolderEntity
from src.data.interface.i_folder_repository import IFolderRepository
from typing import List

class FindAllFolder(IFindAllFolder):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def find(self) -> List[FolderEntity]:
        try:
            result = self.__folder_repository.find_all()
            return result
        except Exception as e:
            raise e from e

