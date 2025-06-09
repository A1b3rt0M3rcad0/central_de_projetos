from src.domain.use_cases.i_find_all_projects_with_basic_details import IFindAllProjectsWithBasicDetails
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.entities.project import ProjectEntity
from typing import List

class FindAllProjectsWithBasicDetails(IFindAllProjectsWithBasicDetails):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repositiry = project_repository
    
    def find(self) -> List[ProjectEntity]:
        try:
            result = self.__project_repositiry.find_all_projects_with_basic_details()
            return result
        except Exception as e:
            raise e from e