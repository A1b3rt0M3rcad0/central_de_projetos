from src.domain.use_cases.i_update_work_project import IUpdateWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from typing import Dict

class UpdateWorkProject(IUpdateWorkProject):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def update(self, work_project_id:int, update_params:Dict) -> None:
        self.__work_project_repository.update(
            work_project_id=work_project_id,
            update_params=update_params
        ) 