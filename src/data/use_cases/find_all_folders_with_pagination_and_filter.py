from src.domain.use_cases.i_find_all_folders_with_pagination_and_filter import IFindAllFoldersWithPaginationAndFilter
from src.domain.entities.folder import FolderEntity
from src.data.interface.i_folder_repository import IFolderRepository
from typing import List

class FindAllFoldersWithPaginationAndFilter(IFindAllFoldersWithPaginationAndFilter):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def find(self, page: int, page_size: int, search_term: str = None) -> List[FolderEntity]:
        try:
            result = self.__folder_repository.find_all_with_pagination_and_filter(
                page=page,
                page_size=page_size,
                search_term=search_term
            )
            return result
        except Exception as e:
            raise e from e

