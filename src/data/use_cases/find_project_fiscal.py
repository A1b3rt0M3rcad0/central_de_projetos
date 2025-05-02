from src.domain.use_cases.i_find_project_fiscal import IFindProjectFiscal
from src.domain.entities.project_fiscal import ProjectFiscalEntity
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

class FindProjectFiscal(IFindProjectFiscal):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository

    def find(self, project_id:int, fiscal_id:int) -> ProjectFiscalEntity:
        try:
            result = self.__project_fiscal_repository.find(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
            return result
        except Exception as e:
            raise e from e