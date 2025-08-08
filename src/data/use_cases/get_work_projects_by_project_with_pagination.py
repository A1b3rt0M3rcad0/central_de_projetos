from src.domain.use_cases.i_get_work_projects_by_project_with_pagination import IGetWorkProjectsByProjectWithPagination
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List

class GetWorkProjectsByProjectWithPagination(IGetWorkProjectsByProjectWithPagination):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_project_with_pagination(self, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        # Buscar todos os work projects do projeto
        all_work_projects = self.__work_project_repository.find_by_project(project_id=project_id)
        
        # Calcular paginação
        total = len(all_work_projects)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        # Aplicar paginação
        paginated_work_projects = all_work_projects[start_index:end_index]
        
        return {
            'total': total,
            'data': paginated_work_projects
        } 