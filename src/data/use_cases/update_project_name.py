from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_name import IUpdateProjectName

class UpdateProjectName(IUpdateProjectName):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:int, name:str) -> None:
        try:
            update_params = {'name': name}
            self.__project_repository.update(
                project_id=project_id,
                update_params=update_params
            )
        except Exception as e:
            raise e from e