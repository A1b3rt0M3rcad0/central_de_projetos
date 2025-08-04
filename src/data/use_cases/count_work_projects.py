from src.domain.use_cases.i_count_work_projects import ICountWorkProjects
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from typing import Dict

class CountWorkProjects(ICountWorkProjects):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def count(self) -> Dict[str, int]:
        return self.__work_project_repository.count_work_projects() 