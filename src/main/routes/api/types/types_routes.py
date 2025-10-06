#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_type_composer import create_type_composer
from src.main.composers.delete_type_composer import delete_type_composer
from src.main.composers.find_type_by_exact_name_composer import find_type_by_exact_name_composer
from src.main.composers.update_type_composer import update_type_composer
from src.main.composers.find_all_types_composer import find_all_types_composer
from src.main.composers.find_all_types_with_pagination_composer import find_all_types_with_pagination_composer
from src.main.composers.find_all_types_with_pagination_and_filter_composer import find_all_types_with_pagination_and_filter_composer

from src.main.routes.api.types.request_format.create_type_format import CreateTypeFormat
from src.main.routes.api.types.request_format.delete_type_format import DeleteTypeFormat
from src.main.routes.api.types.request_format.update_type_format import UpdateTypeFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.types.types_response.find_type_by_exact_name_response import FindTypeByExactNameReponse
from src.main.routes.api.types.types_response.find_all_types_response import FindAllTypesResponse
from src.main.routes.api.types.types_response.find_all_types_with_pagination_response import FindAllTypesWithPaginationResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/types'
TAGS = ['type']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_type(body:CreateTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar um novo tipo de projeto no sistema.
    Apenas usuários ADMIN podem criar tipos.
    
    Args:
        body: Dados do tipo a ser criado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        TypeAlreadyExistsError: Se o tipo já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_type_composer())
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
async def delete_type(body:DeleteTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar um tipo de projeto do sistema.
    Apenas usuários ADMIN podem deletar tipos.
    
    Args:
        body: Dados do tipo a ser deletado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        TypeNotFoundError: Se o tipo não for encontrado
        TypeHasRelatedChildrenError: Se o tipo possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_type_composer())
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
async def update_type(body:UpdateTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o nome de um tipo de projeto.
    Apenas usuários ADMIN podem alterar nomes de tipos.
    
    Args:
        body: Dados para atualização (nome atual e novo nome do tipo)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        TypeNotFoundError: Se o tipo não for encontrado
        TypeAlreadyExistsError: Se já existir um tipo com o novo nome
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_type_composer())
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

@routes.get('/find_by_name/{type_name}', response_model=FindTypeByExactNameReponse, responses=generate_error_responses())
async def find_type_by_exact_name(type_name:str, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar um tipo de projeto específico pelo nome exato.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        type_name: Nome exato do tipo a ser buscado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindTypeByExactNameResponse: Dados do tipo encontrado
        
    Raises:
        TypeNotFoundError: Se o tipo não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['type_name'] = type_name
        http_response = await request_adapter(request, find_type_by_exact_name_composer())
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

@routes.get('/all', response_model=FindAllTypesResponse, responses=generate_error_responses())
async def find_all_types(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os tipos de projeto do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllTypesResponse: Lista com todos os tipos de projeto do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_all_types_composer())
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

@routes.get("/types/pagination/{page_size}/{page}", response_model=FindAllTypesWithPaginationResponse, responses=generate_error_responses())
async def find_all_types_with_pagination(page_size:int, page:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os tipos com paginação.
    Retorna uma lista paginada de tipos para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de tipos por página
        page: Número da página (começa em 1)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllTypesWithPaginationResponse: Lista paginada de tipos com metadados de paginação
        
    Raises:
        InvalidPaginationError: Se os parâmetros de paginação forem inválidos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params["page_size"] = page_size
        request.path_params["page"] = page
        http_response = await request_adapter(request, find_all_types_with_pagination_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level="INFO",
            http_response=http_response,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level="ERROR",
            http_response=error_result,
            logger_name=PREFIX,
            request=request
        )
        return response_adapter(error_result)

@routes.get("/types/pagination-filter/{page_size}/{page}", response_model=FindAllTypesWithPaginationResponse, responses=generate_error_responses())
async def find_all_types_with_pagination_and_filter(page_size:int, page:int, request:Request, search: str = None, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os tipos com paginação e filtro global.
    Retorna uma lista paginada de tipos filtrados para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de tipos por página
        page: Número da página (começa em 1)
        search: Termo de busca opcional para filtrar tipos
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllTypesWithPaginationResponse: Lista paginada de tipos com metadados de paginação
        
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
        http_response = find_all_types_with_pagination_and_filter_composer()(http_request)
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
