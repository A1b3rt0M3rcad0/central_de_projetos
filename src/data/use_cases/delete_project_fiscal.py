from src.domain.use_cases.i_delete_project_fiscal import IDeleteProjectFiscal
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

class DeleteProjectFiscal(IDeleteProjectFiscal):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def delete(self, project_id:int, fiscal_id:int) -> None:
        try:
            self.__project_fiscal_repository.delete(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
        except Exception as e:
            raise e from e