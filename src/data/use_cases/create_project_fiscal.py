from src.domain.use_cases.i_create_project_fiscal import ICreateProjectFiscal
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

class CreateProjectFiscal(ICreateProjectFiscal):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def create(self, project_id:int, fiscal_id:int) -> None:
        try:
            self.__project_fiscal_repository.insert(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
        except Exception as e:
            raise e from e