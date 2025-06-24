from src.domain.use_cases.i_count_projects import ICountProjects
from typing import Dict
from src.data.interface.i_project_repository import IProjectRepository

class CountProjects(ICountProjects):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def count(self) -> Dict[str, int]:
        try:
            return self.__project_repository.count_projects()
        except Exception as e:
            raise e from e