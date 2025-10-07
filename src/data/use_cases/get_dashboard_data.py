"""Get Dashboard Data Use Case"""
#pylint:disable=too-many-branches
from src.domain.use_cases.i_get_dashboard_data import IGetDashboardData
from src.data.interface.i_dashboard_repository import IDashboardRepository
from src.data.interface.i_system_config_repository import ISystemConfigRepository
from typing import Dict, Any, List


class GetDashboardData(IGetDashboardData):
    """Use case para buscar dados do dashboard de forma otimizada"""
    
    def __init__(
        self,
        dashboard_repository: IDashboardRepository,
        system_config_repository: ISystemConfigRepository
    ):
        self.__dashboard_repository = dashboard_repository
        self.__system_config_repository = system_config_repository
    
    def execute(self, modules: List[str] = None, excluded_status_override: List[int] = None) -> Dict[str, Any]:
        """
        Busca dados do dashboard de forma otimizada com filtro de status
        
        Args:
            modules: Lista de módulos a serem buscados. Se None, busca todos
            excluded_status_override: Lista opcional de IDs de status a excluir.
                                     Se None, usa a configuração do sistema
        
        Returns:
            Dict com os dados solicitados e metadata
        """
        # Se modules não for fornecido, busca todos
        if modules is None:
            modules = [
                'counts',
                'projects_by_bairro',
                'budget_by_bairro',
                'projects_by_fiscal',
                'projects_by_empresa',
                'projects_by_user',
                'projects_by_type',
                'projects_by_status',
                'projects_by_bairro_and_type',
                'projects_by_bairro_and_status'
            ]
        
        # Buscar status excluídos da configuração ou usar o override
        if excluded_status_override is not None:
            excluded_status = excluded_status_override
        else:
            excluded_status = self.__system_config_repository.get_dashboard_excluded_status()
        
        # Preparar resposta
        data = {}
        
        # Buscar cada módulo solicitado com filtro de status
        if 'counts' in modules:
            data['counts'] = self.__dashboard_repository.get_counts_summary(excluded_status)
        
        if 'projects_by_bairro' in modules:
            data['projects_by_bairro'] = self.__dashboard_repository.get_projects_by_bairro(excluded_status)
        
        if 'budget_by_bairro' in modules:
            data['budget_by_bairro'] = self.__dashboard_repository.get_budget_by_bairro(excluded_status)
        
        if 'projects_by_fiscal' in modules:
            data['projects_by_fiscal'] = self.__dashboard_repository.get_projects_by_fiscal(excluded_status)
        
        if 'projects_by_empresa' in modules:
            data['projects_by_empresa'] = self.__dashboard_repository.get_projects_by_empresa(excluded_status)
        
        if 'projects_by_user' in modules:
            data['projects_by_user'] = self.__dashboard_repository.get_projects_by_user(excluded_status)
        
        if 'projects_by_type' in modules:
            data['projects_by_type'] = self.__dashboard_repository.get_projects_by_type(excluded_status)
        
        if 'projects_by_status' in modules:
            data['projects_by_status'] = self.__dashboard_repository.get_projects_by_status(excluded_status)
        
        if 'projects_by_bairro_and_type' in modules:
            types_count_data = self.__dashboard_repository.get_projects_by_bairro_and_type(excluded_status)
            types_list = self.__dashboard_repository.get_all_types()
            data['projects_by_bairro_and_type'] = {
                'types': types_list,
                'types_count_by_bairro': types_count_data
            }
        
        if 'projects_by_bairro_and_status' in modules:
            status_count_data = self.__dashboard_repository.get_projects_by_bairro_and_status(excluded_status)
            bairros_list = self.__dashboard_repository.get_all_bairros()
            data['projects_by_bairro_and_status'] = {
                'bairros': bairros_list,
                'status': status_count_data
            }
        
        return {
            'data': data,
            'metadata': {
                'modules_requested': modules,
                'excluded_status': excluded_status,
                'total_modules': len(modules)
            }
        }

