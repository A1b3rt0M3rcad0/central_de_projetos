from src.domain.use_cases.i_update_work_project_title import IUpdateWorkProjectTitle
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class UpdateWorkProjectTitle(IUpdateWorkProjectTitle):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def update(self, work_project_id: int, title: str) -> None:
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        
        self.__work_project_repository.update(
            work_project_id=work_project_id,
            update_params={"title": title.strip()}
        ) 