from abc import ABC, abstractmethod
from typing import Dict, Union, List, Optional
from datetime import datetime
from src.domain.entities.work_project import WorkProjectEntity

class IGetLatestWorkProjectsByFiscal(ABC):
    
    @abstractmethod
    def get_latest_by_fiscal(
        self, 
        fiscal_id: int, 
        page: int, 
        page_size: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Union[int, List[WorkProjectEntity]]]: pass 