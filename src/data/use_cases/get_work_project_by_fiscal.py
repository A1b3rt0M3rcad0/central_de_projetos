from src.domain.use_cases.i_get_work_project_by_fiscal import IGetWorkProjectByFiscal
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity

class GetWorkProjectByFiscal(IGetWorkProjectByFiscal):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get(self, work_project_id: int, fiscal_id: int) -> WorkProjectEntity:
        return self.__work_project_repository.find_by_fiscal_and_id(
            work_project_id=work_project_id,
            fiscal_id=fiscal_id
        ) 