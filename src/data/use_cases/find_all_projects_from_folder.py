from src.domain.use_cases.i_find_all_projects_from_folder import IFindAllProjectsFromFolder
from src.data.interface.i_project_folder_repository import IProjectFolderRepository
from src.domain.entities.project_folder import ProjectFolderEntity
from typing import List

class FindAllProjectsFromFolder(IFindAllProjectsFromFolder):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def find(self, folder_id: int) -> List[ProjectFolderEntity]:
        try:
            results = self.__project_folder_repository.find_all_from_folder(
                folder_id=folder_id
            )
            return results
        except Exception as e:
            raise e from e

