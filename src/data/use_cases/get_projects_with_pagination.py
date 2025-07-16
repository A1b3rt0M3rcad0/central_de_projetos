from src.domain.use_cases.i_get_projects_with_pagination import IGetProjectsWithPagination
from src.data.interface.i_project_repository import IProjectRepository
from typing import Dict, Union
from src.domain.entities.project import ProjectEntity

class GetProjectsWithPagination(IGetProjectsWithPagination):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def get(self, page:int, page_size:int = 10) -> Dict[int, Union[int, ProjectEntity]]:
        try:
            result = self.__project_repository.get_projects_with_pagination(page=page, page_size=page_size)
            return result
        except Exception as e:
            raise e from e