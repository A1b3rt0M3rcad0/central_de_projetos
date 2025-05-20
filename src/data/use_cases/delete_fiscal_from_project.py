from src.domain.use_cases.i_delete_fiscal_from_project import IDeleteFiscalFromProject
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository

class DeleteFiscalFromProject(IDeleteFiscalFromProject):

    def __init__(self, project_fiscal_repository:IProjectFiscalRepository) -> None:
        self.__project_fiscal_repository = project_fiscal_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_fiscal_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e