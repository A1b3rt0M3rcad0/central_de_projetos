from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity

class GetWorkProject(IGetWorkProject):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get(self, work_project_id:int) -> WorkProjectEntity:
        return self.__work_project_repository.find(work_project_id=work_project_id) 