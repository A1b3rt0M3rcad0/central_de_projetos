from src.domain.use_cases.i_find_project_folder import IFindProjectFolder
from src.domain.entities.project_folder import ProjectFolderEntity
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

class FindProjectFolder(IFindProjectFolder):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def find(self, project_id: int, folder_id: int) -> ProjectFolderEntity:
        try:
            result = self.__project_folder_repository.find(
                project_id=project_id,
                folder_id=folder_id
            )
            return result
        except Exception as e:
            raise e from e

