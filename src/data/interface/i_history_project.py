from abc import ABC, abstractmethod
from src.domain.entities.history_project import HistoryProjectEntity
from typing import List, Dict, Optional

class IHistoryProjectRepository(ABC):

    @abstractmethod
    def insert(self, project_id:int, column_name:str, description:Optional[str]=None) -> None:pass

    @abstractmethod
    def find(self, history_project_id:int) -> HistoryProjectEntity:pass

    @abstractmethod
    def find_all_from_project(self, project_id:int) -> List[HistoryProjectEntity]:pass

    @abstractmethod
    def update(self, history_project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, history_project_id:int) -> None:pass