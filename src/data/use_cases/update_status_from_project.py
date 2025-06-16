from src.domain.use_cases.i_update_status_from_project import IUpdateStatusFromProject
from src.data.interface.i_project_repository import IProjectRepository

class UpdateStatusFromProject(IUpdateStatusFromProject):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:int, status_id:int) -> None:
        try:
            self.__project_repository.update(
                project_id=project_id,
                update_params={
                    'status_id': status_id
                }
            )
        except Exception as e:
            raise e from e