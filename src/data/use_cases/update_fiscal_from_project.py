from src.domain.use_cases.i_update_fiscal_from_project import IUpdateFiscalFromProject
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

class UpdateFiscalFromProject(IUpdateFiscalFromProject):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def update(self, project_id:int, fiscal_id:int, new_fiscal_id:int) -> None:
        try:
            self.__project_fiscal_repository.update_fiscal(
                project_id=project_id,
                fiscal_id=fiscal_id,
                new_fiscal_id=new_fiscal_id
            )
        except Exception as e:
            raise e from e