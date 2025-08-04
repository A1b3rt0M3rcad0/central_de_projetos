from src.domain.use_cases.i_get_work_projects_with_pagination import IGetWorkProjectsWithPagination
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List

class GetWorkProjectsWithPagination(IGetWorkProjectsWithPagination):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        return self.__work_project_repository.get_work_projects_with_pagination(
            page=page,
            page_size=page_size
        ) 