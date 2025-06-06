from abc import ABC, abstractmethod
from src.domain.value_objects.monetary_value import MonetaryValue
from datetime import datetime
from typing import Optional, List, Dict
from src.domain.entities.project import ProjectEntity

class IProjectRepository(ABC):
    
    @abstractmethod
    def insert(self, status_id:int, name:str|None=None, verba_disponivel:Optional[MonetaryValue]=None, andamento_do_projeto:Optional[str]=None, start_date:Optional[datetime]=None, expected_completion_date:Optional[datetime]=None, end_date:Optional[datetime]=None) -> None:pass

    @abstractmethod
    def find(self, project_id:int) -> ProjectEntity:pass

    @abstractmethod
    def find_all(self) -> List[ProjectEntity]:pass

    @abstractmethod
    def find_by_status(self, status_id:int) -> List[Optional[ProjectEntity]]:pass

    @abstractmethod
    def find_by_name(self, name:str) -> ProjectEntity:pass

    @abstractmethod
    def find_all_from_project(self, project_id:int) -> ProjectEntity:pass

    @abstractmethod
    def update(self, project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, project_id:int) -> None:pass