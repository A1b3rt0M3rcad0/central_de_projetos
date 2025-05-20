from src.domain.use_cases.i_delete_history_project import IDeleteHistoryProject
from src.data.interface.i_history_project_repository import IHistoryProjectRepository

class DeleteHistoryProject(IDeleteHistoryProject):

    def __init__(self, history_project_repository:IHistoryProjectRepository) -> None:
        self.__history_project_repository = history_project_repository
    
    def delete(self, history_project_id:int) -> None:
        try:
            self.__history_project_repository.delete(
                history_project_id=history_project_id
            )
        except Exception as e:
            raise e from e