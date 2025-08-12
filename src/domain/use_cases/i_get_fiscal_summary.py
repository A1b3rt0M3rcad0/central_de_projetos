from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class IGetFiscalSummary(ABC):
    
    @abstractmethod
    def get_summary(
        self, 
        fiscal_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """Get fiscal summary with statistics and recent activity"""