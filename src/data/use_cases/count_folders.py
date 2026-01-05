from src.domain.use_cases.i_count_folders import ICountFolders
from src.data.interface.i_folder_repository import IFolderRepository

class CountFolders(ICountFolders):

    def __init__(self, folder_repository: IFolderRepository) -> None:
        self.__folder_repository = folder_repository
    
    def count(self, search_term: str = None) -> int:
        try:
            if search_term:
                result = self.__folder_repository.count_all_with_filter(
                    search_term=search_term
                )
            else:
                result = self.__folder_repository.count_all()
            return result
        except Exception as e:
            raise e from e

