#pylint:disable=W0718
#pylint:disable=W0613
"""Dashboard routes"""
from fastapi import APIRouter, Request, Security, Query
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler
from src.main.composers.get_dashboard_data_composer import get_dashboard_data_composer
from src.main.routes.api.dashboard.dashboard_response.get_dashboard_data_response import DashboardDataResponse
from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.middleware.authorization import role_required
from src.logs.log_http import log_http
from src.main.routes.middleware.insert_access_token import insert_access_token

PREFIX = "api.dashboard"
routes = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@routes.get(
    "/data",
    response_model=DashboardDataResponse,
    responses=generate_error_responses(),
    summary="Buscar dados do dashboard otimizado",
    description="""
    Endpoint unificado para buscar todos os dados do dashboard em uma única requisição.
    
    **Benefícios:**
    - ⚡ Performance otimizada (1 requisição vs 11 requisições)
    - 🔄 Dados consistentes do mesmo momento
    - 🎯 Módulos sob demanda
    - 📊 Filtro configurável de status excluídos
    
    **Módulos disponíveis:**
    - `counts`: Contagens gerais (projetos, bairros, empresas, fiscais)
    - `projects_by_bairro`: Número de projetos por bairro
    - `budget_by_bairro`: Orçamento total por bairro
    - `projects_by_fiscal`: Número de projetos por fiscal
    - `projects_by_empresa`: Número de projetos por empresa
    - `projects_by_user`: Número de projetos por usuário (vereador)
    - `projects_by_type`: Número de projetos por tipo
    - `projects_by_status`: Número de projetos por status
    - `projects_by_bairro_and_type`: Projetos agrupados por bairro e tipo
    - `projects_by_bairro_and_status`: Projetos agrupados por bairro e status
    
    **Filtro de Status:**
    - Por padrão, usa a configuração `dashboard.excluded_status` do sistema
    - Pode ser sobrescrito via parâmetro `excluded_status`
    - Exemplo: excluir projetos "Finalizados" ou "Cancelados"
    """
)
async def get_dashboard_data(
    request: Request,
    modules: str = Query(
        None,
        description="Módulos separados por vírgula. Ex: 'counts,projects_by_bairro'. Se omitido, retorna todos"
    ),
    excluded_status: str = Query(
        None,
        description="IDs de status a excluir separados por vírgula. Ex: '1,3,5'. Se omitido, usa configuração do sistema"
    ),
    user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))
):
    """
    Endpoint unificado para dados do dashboard com filtro de status configurável
    
    Args:
        request: Objeto da requisição HTTP
        modules: String com módulos separados por vírgula
        excluded_status: String com IDs de status a excluir separados por vírgula
        user: Dados do usuário autenticado (injetado pelo middleware)
    
    Returns:
        DashboardDataResponse: Dados do dashboard com metadata
    
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    
    Examples:
        - Buscar todos os módulos: GET /dashboard/data
        - Buscar apenas contagens: GET /dashboard/data?modules=counts
        - Excluir status finalizados: GET /dashboard/data?excluded_status=8,10
        - Combinado: GET /dashboard/data?modules=counts,projects_by_bairro&excluded_status=8
    """
    try:
        # Criar HttpRequest
        from src.presentation.http_types.http_request import HttpRequest
        http_request = HttpRequest(
            body={},
            headers=dict(request.headers),
            query_params={
                "modules": modules,
                "excluded_status": excluded_status
            },
            path_params={},
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = get_dashboard_data_composer()(http_request)
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        
        log_http(
            level="INFO",
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        
        return response_adapter(http_response)
    except Exception as exception:
        error_result = error_handler(exception)
        log_http(
            level="ERROR",
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

