from src.data.interface.i_history_project_repository import IHistoryProjectRepository
from src.domain.use_cases.i_find_all_history_from_project import IFindAllHistoryFromProject
from src.domain.entities.history_project import HistoryProjectEntity
from typing import List

class FindAllHistoryFromProject(IFindAllHistoryFromProject):

    def __init__(self, history_project_repository:IHistoryProjectRepository) -> None:
        self.__history_project_repository = history_project_repository
    
    def find(self, project_id:int) -> List[HistoryProjectEntity]:
        try:
            result = self.__history_project_repository.find_all_from_project(
                project_id=project_id
            )
            return result
        except Exception as e:
            raise e from e