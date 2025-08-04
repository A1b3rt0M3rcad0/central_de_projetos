from src.domain.use_cases.i_delete_work_project import IDeleteWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class DeleteWorkProject(IDeleteWorkProject):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def delete(self, work_project_id:int) -> None:
        self.__work_project_repository.delete(work_project_id=work_project_id) 