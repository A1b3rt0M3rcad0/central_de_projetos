from src.domain.use_cases.i_find_all_projects_from_fiscal import IFindAllProjectsFromFiscal
from typing import List
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class FindAllProjectsFromFiscal(IFindAllProjectsFromFiscal):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def find(self, fiscal_id) -> List[ProjectFiscalEntity]:
        try:
            results = self.__project_fiscal_repository.find_all_from_fiscal(
                fiscal_id=fiscal_id
            )
            return results
        except Exception as e:
            raise e from e