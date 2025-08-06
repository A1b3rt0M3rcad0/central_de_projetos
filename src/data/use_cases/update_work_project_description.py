from src.domain.use_cases.i_update_work_project_description import IUpdateWorkProjectDescription
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class UpdateWorkProjectDescription(IUpdateWorkProjectDescription):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def update(self, work_project_id: int, description: str) -> None:
        if not description or len(description.strip()) == 0:
            raise ValueError("Description cannot be empty")
        
        self.__work_project_repository.update(
            work_project_id=work_project_id,
            update_params={"description": description.strip()}
        ) 