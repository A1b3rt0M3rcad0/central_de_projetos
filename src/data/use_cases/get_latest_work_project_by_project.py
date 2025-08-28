from src.domain.use_cases.i_get_latest_work_project_by_project import IGetLatestWorkProjectByProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Optional

class GetLatestWorkProjectByProject(IGetLatestWorkProjectByProject):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_latest_by_project(self, project_id: int) -> Optional[WorkProjectEntity]:
        return self.__work_project_repository.find_latest_by_project(project_id=project_id) 