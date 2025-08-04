from src.domain.use_cases.i_get_work_projects_by_project_and_fiscal import IGetWorkProjectsByProjectAndFiscal
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import List

class GetWorkProjectsByProjectAndFiscal(IGetWorkProjectsByProjectAndFiscal):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_project_and_fiscal(self, project_id:int, fiscal_id:int) -> List[WorkProjectEntity]:
        return self.__work_project_repository.find_by_project_and_fiscal(
            project_id=project_id,
            fiscal_id=fiscal_id
        ) 