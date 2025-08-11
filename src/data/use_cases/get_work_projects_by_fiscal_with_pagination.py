from src.domain.use_cases.i_get_work_projects_by_fiscal_with_pagination import IGetWorkProjectsByFiscalWithPagination
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List

class GetWorkProjectsByFiscalWithPagination(IGetWorkProjectsByFiscalWithPagination):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_fiscal_with_pagination(self, fiscal_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        # Usar o método eficiente do repositório que faz paginação no banco de dados
        return self.__work_project_repository.get_work_projects_with_pagination_by_fiscal(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size
        ) 