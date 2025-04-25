from src.domain.entities.project import ProjectEntity
from typing import List
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_find_project_by_status import IFindProjectByStatus

class FindProjectByStatus(IFindProjectByStatus):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def find(self, status_id:int) -> List[ProjectEntity]:
        try:
            result = self.__project_repository.find_by_status(
                status_id=status_id
            )
            return result
        except Exception as e:
            raise e from e