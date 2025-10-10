from datetime import datetime
from src.errors.eap.base_eap_error import BaseEAPError


def _normalize_datetime(dt: datetime) -> datetime:
    """Remove timezone information from datetime for comparison"""
    if dt is None:
        return None
    # Converte para date (apenas dia/mês/ano, sem hora) para comparação
    # Isso resolve problemas de timezone
    if hasattr(dt, 'date'):
        return dt.date()
    return dt


class InvalidDateRangeError(BaseEAPError):
    """Erro quando as datas do item filho violam as datas do item pai"""
    
    def __init__(self, child_name: str, parent_name: str, 
                 child_start: datetime, child_end: datetime,
                 parent_start: datetime, parent_end: datetime):
        self.child_name = child_name
        self.parent_name = parent_name
        self.child_start = child_start
        self.child_end = child_end
        self.parent_start = parent_start
        self.parent_end = parent_end
        
        # Normaliza as datas para comparação e formatação
        child_start_norm = _normalize_datetime(child_start)
        child_end_norm = _normalize_datetime(child_end)
        parent_start_norm = _normalize_datetime(parent_start)
        parent_end_norm = _normalize_datetime(parent_end)
        
        message = f"Datas inválidas para o item '{child_name}'. "
        
        if child_start_norm < parent_start_norm:
            message += f"Data de início ({child_start_norm.strftime('%d/%m/%Y')}) não pode ser anterior à data de início do pai '{parent_name}' ({parent_start_norm.strftime('%d/%m/%Y')}). "
        
        if child_end_norm > parent_end_norm:
            message += f"Data de término ({child_end_norm.strftime('%d/%m/%Y')}) não pode ser posterior à data de término do pai '{parent_name}' ({parent_end_norm.strftime('%d/%m/%Y')}). "
        
        super().__init__(
            status_code=400,
            message=message.strip()
        )

