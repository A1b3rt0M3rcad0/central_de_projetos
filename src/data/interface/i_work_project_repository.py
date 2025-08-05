from abc import ABC, abstractmethod
from typing import List, Dict, Union
from src.domain.entities.work_project import WorkProjectEntity

class IWorkProjectRepository(ABC):
    
    @abstractmethod
    def insert(self, project_id:int, fiscal_id:int, title:str, description:str, photo_name:str, additional_documents:str=None) -> int:pass

    @abstractmethod
    def find(self, work_project_id:int) -> WorkProjectEntity:pass

    @abstractmethod
    def find_all(self) -> List[WorkProjectEntity]:pass

    @abstractmethod
    def find_by_project(self, project_id:int) -> List[WorkProjectEntity]:pass

    @abstractmethod
    def find_by_fiscal(self, fiscal_id:int) -> List[WorkProjectEntity]:pass

    @abstractmethod
    def find_by_project_and_fiscal(self, project_id:int, fiscal_id:int) -> List[WorkProjectEntity]:pass

    @abstractmethod
    def find_by_title(self, title:str) -> WorkProjectEntity:pass

    @abstractmethod
    def count_work_projects(self) -> Dict[str, int]:pass

    @abstractmethod
    def get_work_projects_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, WorkProjectEntity]]:pass

    @abstractmethod
    def update(self, work_project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, work_project_id:int) -> None:pass 