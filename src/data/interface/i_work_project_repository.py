from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional
from src.domain.entities.work_project import WorkProjectEntity
from datetime import datetime

class IWorkProjectRepository(ABC):
    
    @abstractmethod
    def insert(self, project_id:int, fiscal_id:int, title:str, description:str, photo_name:str, additional_documents=None) -> int:pass

    @abstractmethod
    def find(self, work_project_id:int) -> WorkProjectEntity:pass

    @abstractmethod
    def find_by_fiscal_and_id(self, work_project_id:int, fiscal_id:int) -> WorkProjectEntity:pass

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
    def find_by_title_and_fiscal(self, title:str, fiscal_id:int) -> WorkProjectEntity:pass

    @abstractmethod
    def find_latest_by_project(self, project_id:int) -> Optional[WorkProjectEntity]:pass

    @abstractmethod
    def count_work_projects(self) -> Dict[str, int]:pass

    @abstractmethod
    def get_work_projects_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, WorkProjectEntity]]:pass

    @abstractmethod
    def get_work_projects_with_pagination_by_fiscal(self, fiscal_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass

    @abstractmethod
    def get_work_projects_with_pagination_by_fiscal_and_project(self, fiscal_id:int, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass

    @abstractmethod
    def get_work_projects_with_pagination_by_project(self, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass

    @abstractmethod
    def get_latest_work_projects_by_fiscal_with_date_filter(
        self, 
        fiscal_id: int, 
        page: int, 
        page_size: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Union[int, List[WorkProjectEntity]]]: pass

    @abstractmethod
    def update(self, work_project_id:int, update_params:Dict) -> None:pass

    @abstractmethod
    def delete(self, work_project_id:int) -> None:pass
    
    @abstractmethod
    def delete_all_from_project(self, project_id:int) -> None:pass
    
    @abstractmethod
    def delete_all_from_fiscal(self, fiscal_id:int) -> None:
        """Deleta todos os work projects associados a um fiscal""" 