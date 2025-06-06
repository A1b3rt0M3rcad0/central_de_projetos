from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_find_all_from_project import IFindAllFromProject
from src.domain.entities.project import ProjectEntity

from src.errors.repository.error_on_find.error_on_find_project import ErrorOnFindProject

class FindAllFromProject(IFindAllFromProject):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def find(self, project_id:int) -> ProjectEntity:
        try:
            result = self.__project_repository.find_all_from_project(project_id=project_id)
            return result
        except Exception as e: 
            raise ErrorOnFindProject(
                message=f"Error on find project project_id={project_id}"
            ) from e