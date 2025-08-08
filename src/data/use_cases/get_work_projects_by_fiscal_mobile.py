from src.domain.use_cases.i_get_work_projects_by_fiscal_mobile import IGetWorkProjectsByFiscalMobile
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List

class GetWorkProjectsByFiscalMobile(IGetWorkProjectsByFiscalMobile):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_fiscal_mobile(self, fiscal_id:int, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        # Buscar work projects do fiscal para o projeto específico
        work_projects = self.__work_project_repository.find_by_project_and_fiscal(
            project_id=project_id,
            fiscal_id=fiscal_id
        )
        
        # Calcular paginação
        total = len(work_projects)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        # Aplicar paginação
        paginated_work_projects = work_projects[start_index:end_index]
        
        return {
            'total': total,
            'data': paginated_work_projects
        } 