from src.domain.use_cases.i_get_work_projects_by_project_with_pagination import IGetWorkProjectsByProjectWithPagination
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List

class GetWorkProjectsByProjectWithPagination(IGetWorkProjectsByProjectWithPagination):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_project_with_pagination(self, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        # Usar o método específico do repository para paginação por projeto
        result = self.__work_project_repository.get_work_projects_with_pagination_by_project(
            project_id=project_id,
            page=page,
            page_size=page_size
        )
        
        return {
            'total': result['total'],
            'data': result['data']
        } 