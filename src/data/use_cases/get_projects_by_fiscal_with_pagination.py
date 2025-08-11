from src.domain.use_cases.i_get_projects_by_fiscal_with_pagination import IGetProjectsByFiscalWithPagination
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository
from typing import Dict, Union, List
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class GetProjectsByFiscalWithPagination(IGetProjectsByFiscalWithPagination):

    def __init__(self, project_fiscal_repository: IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def get(self, fiscal_id: int, page: int, page_size: int = 10) -> Dict[str, Union[int, List[ProjectFiscalEntity]]]:
        try:
            result = self.__project_fiscal_repository.get_projects_by_fiscal_with_pagination(
                fiscal_id=fiscal_id, 
                page=page, 
                page_size=page_size
            )
            return result
        except Exception as e:
            raise e from e 