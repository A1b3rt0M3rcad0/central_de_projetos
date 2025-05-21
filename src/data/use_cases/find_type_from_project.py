from src.domain.entities.project_types import ProjectTypeEntity
from src.domain.use_cases.i_find_type_from_project import IFindTypeFromProject
from src.data.interface.i_project_type_repository import IProjectTypeRepository
from typing import List

class FindTypeFromProject(IFindTypeFromProject):

    def __init__(self, project_type_repository:IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def find(self, project_id:int) -> List[ProjectTypeEntity]:
        try:
            associations = self.__project_type_repository.select_all_from_project(
                project_id=project_id
            )
            return associations
        except Exception as e:
            raise e from e