from src.domain.use_cases.i_get_work_projects_by_fiscal import IGetWorkProjectsByFiscal
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import List

class GetWorkProjectsByFiscal(IGetWorkProjectsByFiscal):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_fiscal(self, fiscal_id:int) -> List[WorkProjectEntity]:
        return self.__work_project_repository.find_by_fiscal(fiscal_id=fiscal_id) 