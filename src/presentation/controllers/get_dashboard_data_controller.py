#pylint:disable=all
"""Get Dashboard Data Controller"""
from src.domain.use_cases.i_get_dashboard_data import IGetDashboardData
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class GetDashboardDataController(ControllerInterface):
    """Controller para buscar dados do dashboard de forma otimizada"""
    
    def __init__(self, get_dashboard_data_use_case: IGetDashboardData) -> None:
        self.__get_dashboard_data_use_case = get_dashboard_data_use_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Processa requisição de dados do dashboard
        
        Query params aceitos:
            - modules: string com módulos separados por vírgula (ex: "counts,projects_by_bairro")
            - excluded_status: string com IDs separados por vírgula (ex: "1,3,5")
        """
        try:
            query_params = http_request.query_params
            
            # Parse módulos solicitados
            modules_param = query_params.get('modules')
            modules = None
            if modules_param:
                modules = [m.strip() for m in modules_param.split(',') if m.strip()]
            
            # Parse status excluídos (override da configuração)
            excluded_status_param = query_params.get('excluded_status')
            excluded_status_override = None
            if excluded_status_param:
                excluded_status_override = [
                    int(s.strip()) 
                    for s in excluded_status_param.split(',') 
                    if s.strip().isdigit()
                ]
            
            # Executar use case
            result = self.__get_dashboard_data_use_case.execute(
                modules=modules,
                excluded_status_override=excluded_status_override
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Dashboard data retrieved successfully',
                    'content': result['data'],
                    'metadata': result['metadata']
                }
            )
        except Exception as e:
            raise e from e

