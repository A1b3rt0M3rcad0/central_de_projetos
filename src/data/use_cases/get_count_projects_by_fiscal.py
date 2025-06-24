from src.domain.use_cases.i_get_count_projects_by_fiscal import IGetCountProjectsByFiscal
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository
from typing import Dict

class GetCountProjectsByFiscal(IGetCountProjectsByFiscal):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def get(self) -> Dict[str, int]:
        try:
            result = self.__project_fiscal_repository.get_count_projects_by_fiscal()
            return result
        except Exception as e:
            raise e from e