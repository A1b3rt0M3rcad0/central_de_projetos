from src.domain.use_cases.i_delete_all_projects_from_folder import IDeleteAllProjectsFromFolder
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

class DeleteAllProjectsFromFolder(IDeleteAllProjectsFromFolder):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def delete(self, folder_id: int) -> None:
        try:
            self.__project_folder_repository.delete_all_from_folder(
                folder_id=folder_id
            )
        except Exception as e:
            raise e from e

