from src.domain.use_cases.i_delete_project_folder import IDeleteProjectFolder
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

class DeleteProjectFolder(IDeleteProjectFolder):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def delete(self, project_id: int, folder_id: int) -> None:
        try:
            self.__project_folder_repository.delete(
                project_id=project_id,
                folder_id=folder_id
            )
        except Exception as e:
            raise e from e

