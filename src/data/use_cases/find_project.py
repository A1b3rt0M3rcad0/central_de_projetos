from src.domain.entities.project import ProjectEntity
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_find_project import IFindProject
from src.errors.use_cases.project_not_found_error import ProjectNotFoundError

class FindProject(IFindProject):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def find(self, project_id:int) -> ProjectEntity:
        try:
            result = self.__project_repository.find(
                project_id=project_id
            )
            return result
        except AttributeError as e:
            raise ProjectNotFoundError(message=f'Project with id {project_id} not founded: {e}') from e
        except Exception as e:
            raise e from e