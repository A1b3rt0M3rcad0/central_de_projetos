from src.domain.use_cases.i_find_all_folders_with_pagination import IFindAllFoldersWithPagination
from src.domain.entities.folder import FolderEntity
from src.data.interface.i_folder_repository import IFolderRepository
from typing import List

class FindAllFoldersWithPagination(IFindAllFoldersWithPagination):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def find(self, page: int, page_size: int) -> List[FolderEntity]:
        try:
            result = self.__folder_repository.find_all_with_pagination(
                page=page,
                page_size=page_size
            )
            return result
        except Exception as e:
            raise e from e

