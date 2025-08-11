from src.domain.use_cases.i_get_latest_work_projects_by_fiscal import IGetLatestWorkProjectsByFiscal
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.domain.entities.work_project import WorkProjectEntity
from typing import Dict, Union, List, Optional
from datetime import datetime

class GetLatestWorkProjectsByFiscal(IGetLatestWorkProjectsByFiscal):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def get_latest_by_fiscal(
        self, 
        fiscal_id: int, 
        page: int, 
        page_size: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Union[int, List[WorkProjectEntity]]]:
        # Usar o método eficiente do repositório que faz paginação no banco de dados
        return self.__work_project_repository.get_latest_work_projects_by_fiscal_with_date_filter(
            fiscal_id=fiscal_id,
            page=page,
            page_size=page_size,
            start_date=start_date,
            end_date=end_date
        ) 