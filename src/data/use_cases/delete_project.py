from src.domain.use_cases.i_delete_project import IDeleteProject
from src.data.interface.i_project_repository import IProjectRepository

class DeleteProject(IDeleteProject):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_repository.delete(
                project_id=project_id
            )
        except Exception as e:
            raise e from e