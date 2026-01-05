#pylint:disable=W0718
#pylint:disable=W0613,W9016
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_status_composer import find_status_composer
from src.main.composers.create_status_composer import create_status_composer
from src.main.composers.delete_status_composer import delete_status_composer
from src.main.composers.update_status_description_composer import update_status_description_composer
from src.main.composers.find_all_status_composer import find_all_status_composer
from src.main.composers.find_project_by_status_composer import find_project_by_status_composer
from src.main.composers.find_all_status_with_pagination_composer import find_all_status_with_pagination_composer
from src.main.composers.find_all_status_with_pagination_and_filter_composer import find_all_status_with_pagination_and_filter_composer

from src.main.routes.api.status.format_request.create_status_format import CreateStatusFormat
from src.main.routes.api.status.format_request.delete_status_format import DeleteStatusFormat
from src.main.routes.api.status.format_request.update_status_description_format import UpdateStatusDescriptionFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.status.status_response.find_status_response import FindStatusReponse
from src.main.routes.api.status.status_response.find_all_status_response import FindAllStatusResponse
from src.main.routes.api.status.status_response.find_project_by_status_response import FindProjectbyStatusReponse
from src.main.routes.api.status.status_response.find_all_status_with_pagination_response import FindAllStatusWithPaginationResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/status'
TAGS = ['status']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

# IMPORTANTE: Rotas específicas (como /all) devem vir ANTES de rotas com parâmetros (como /{status_id})
# O FastAPI faz match na ordem de definição, então /all precisa vir antes de /{status_id}

@routes.get('/all', response_model=FindAllStatusResponse, responses=generate_error_responses())
async def find_all_status(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os status do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllStatusResponse: Lista com todos os status do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_all_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/{status_id}', response_model=FindStatusReponse, responses=generate_error_responses())
async def find_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar um status específico pelo ID.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        status_id: ID do status a ser buscado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindStatusResponse: Dados do status encontrado
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_status(body:CreateStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar um novo status no sistema.
    Apenas usuários com permissões de ADMIN podem acessar.
    
    Args:
        body: Dados do status a ser criado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Confirmação de criação do status
        
    Raises:
        StatusAlreadyExistsError: Se já existir um status com a mesma descrição
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.delete('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_status(body:DeleteStatusFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para excluir um status do sistema.
    Apenas usuários com permissões de ADMIN podem acessar.
    
    Args:
        body: Dados do status a ser excluído
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Confirmação de exclusão do status
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        StatusInUseError: Se o status estiver sendo usado em projetos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)
    
@routes.patch('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_status_description(body:UpdateStatusDescriptionFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar a descrição de um status existente.
    Apenas usuários com permissões de ADMIN podem acessar.
    
    Args:
        body: Dados do status a ser atualizado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Confirmação de atualização do status
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        StatusAlreadyExistsError: Se já existir outro status com a mesma descrição
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_status_description_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/pagination/{page_size}/{page}', response_model=FindAllStatusWithPaginationResponse, responses=generate_error_responses())
async def find_all_status_with_pagination(page_size:int, page:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar status com paginação.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de itens por página
        page: Número da página
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllStatusWithPaginationResponse: Lista paginada de status
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['page_size'] = page_size
        request.path_params['page'] = page
        http_response = await request_adapter(request, find_all_status_with_pagination_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/projects/{status_id}', response_model=FindProjectbyStatusReponse, responses=generate_error_responses())
async def find_project_by_status(status_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar projetos filtrados por status.
    Retorna todos os projetos que possuem o status especificado.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        status_id: ID do status para filtrar os projetos
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindProjectByStatusResponse: Lista de projetos com o status especificado
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['status_id'] = status_id
        http_response = await request_adapter(request, find_project_by_status_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)
@routes.get("/pagination-filter/{page_size}/{page}", response_model=FindAllStatusWithPaginationResponse, responses=generate_error_responses())
async def find_all_status_with_pagination_and_filter(page_size:int, page:int, request:Request, search: str = None, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os status com paginação e filtro global.
    Retorna uma lista paginada de status filtrados para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de status por página
        page: Número da página (começa em 1)
        search: Termo de busca opcional para filtrar status
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllStatusWithPaginationResponse: Lista paginada de status com metadados de paginação
        
    Raises:
        InvalidPaginationError: Se os parâmetros de paginação forem inválidos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        # Criar um novo request com os parâmetros
        from src.presentation.http_types.http_request import HttpRequest
        http_request = HttpRequest(
            body={},
            headers=dict(request.headers),
            query_params={
                "search": search
            },
            path_params={
                "page_size": page_size,
                "page": page
            },
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = find_all_status_with_pagination_and_filter_composer()(http_request)
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level="INFO",
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level="ERROR",
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)
