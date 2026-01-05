from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IGetDashboardData(ABC):
    """Interface para buscar dados do dashboard"""
    
    @abstractmethod
    def execute(self, modules: List[str] = None, excluded_status_override: List[int] = None) -> Dict[str, Any]:
        """
        Busca dados do dashboard de forma otimizada com filtro de status
        
        Args:
            modules: Lista de módulos a serem buscados. 
                     Opções: 'counts', 'projects_by_bairro', 'budget_by_bairro', 
                            'projects_by_fiscal', 'projects_by_empresa', 'projects_by_user',
                            'projects_by_bairro_and_type', 'projects_by_bairro_and_status'
                     Se None, busca todos os módulos
            excluded_status_override: Lista opcional de IDs de status a excluir.
                                     Se None, usa a configuração do sistema (dashboard.excluded_status)
        
        Returns:
            Dict com os dados solicitados e metadata (incluindo excluded_status aplicado)
        """
        pass

