from src.domain.entities.project import ProjectEntity
from src.domain.use_cases.i_find_all_project import IFindAllProjects
from src.data.interface.i_project_repository import IProjectRepository
from typing import List

class FindAllProjects(IFindAllProjects):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def find(self) -> List[ProjectEntity]:
        try:
            results = self.__project_repository.find_all()
            return results
        except Exception as e:
            raise e from e