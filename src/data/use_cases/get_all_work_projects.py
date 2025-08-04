from src.domain.use_cases.i_get_all_work_projects import IGetAllWorkProjects
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import List

class GetAllWorkProjects(IGetAllWorkProjects):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_all(self) -> List[WorkProjectEntity]:
        return self.__work_project_repository.find_all() 