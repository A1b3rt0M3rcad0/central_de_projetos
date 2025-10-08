from src.domain.use_cases.i_find_all_projects_from_type import IFindAllProjectsFromType
from src.data.interface.i_project_type_repository import IProjectTypeRepository
from src.domain.entities.project_type import ProjectTypeEntity
from typing import List

class FindAllProjectsFromType(IFindAllProjectsFromType):

    def __init__(self, project_type_repository: IProjectTypeRepository) -> None:
        self.__project_type_repository = project_type_repository
    
    def find(self, type_id: int) -> List[ProjectTypeEntity]:
        try:
            result = self.__project_type_repository.find_all_from_type(
                type_id=type_id
            )
            return result
        except Exception as e:
            raise e from e

