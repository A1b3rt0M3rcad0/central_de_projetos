from src.domain.use_cases.i_get_work_project_by_title import IGetWorkProjectByTitle
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity

class GetWorkProjectByTitle(IGetWorkProjectByTitle):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_by_title(self, title:str) -> WorkProjectEntity:
        return self.__work_project_repository.find_by_title(title=title) 