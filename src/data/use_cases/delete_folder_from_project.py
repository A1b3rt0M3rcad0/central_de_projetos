from src.domain.use_cases.i_delete_folder_from_project import IDeleteFolderFromProject
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

class DeleteFolderFromProject(IDeleteFolderFromProject):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def delete(self, project_id: int) -> None:
        try:
            self.__project_folder_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e

