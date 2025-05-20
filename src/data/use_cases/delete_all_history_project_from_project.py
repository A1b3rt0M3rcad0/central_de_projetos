from src.domain.use_cases.i_delete_all_history_project_from_project import IDeleteAllHistoryProjectFromProject
from src.data.interface.i_history_project_repository import IHistoryProjectRepository

class DeleteAllHistoryProjectFromProject(IDeleteAllHistoryProjectFromProject):

    def __init__(self, history_project_repository:IHistoryProjectRepository) -> None:
        self.__history_project_repository = history_project_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__history_project_repository.delete_all_from_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e