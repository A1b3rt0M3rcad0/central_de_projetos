from src.domain.use_cases.i_delete_work_project_from_project import IDeleteWorkProjectFromProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class DeleteWorkProjectFromProject(IDeleteWorkProjectFromProject):

    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def delete(self, project_id: int) -> None:
        try:
            self.__work_project_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e

