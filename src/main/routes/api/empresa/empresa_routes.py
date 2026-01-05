#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_empresa_by_exact_name_composer import find_empresa_by_exact_name_composer
from src.main.composers.find_all_empresas_composer import find_empresas_composer
from src.main.composers.create_empresa_composer import create_empresa_composer
from src.main.composers.delete_empresa_composer import delete_empresa_composer
from src.main.composers.update_empresa_composer import update_empresas_composer
from src.main.composers.count_empresas_composer import count_empresas_composer
from src.main.composers.find_all_empresas_with_pagination_composer import find_all_empresas_with_pagination_composer
from src.main.composers.find_all_empresas_with_pagination_and_filter_composer import find_all_empresas_with_pagination_and_filter_composer

from src.main.routes.api.empresa.request_format.create_empresa_format import CreateEmpresaFormat
from src.main.routes.api.empresa.request_format.delete_empresa_format import DeleteEmpresaFormat
from src.main.routes.api.empresa.request_format.update_empresas_composer import UpdateEmpresasFormat
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.empresa.empresa_response.find_empresa_response import FindEmpresaResponse
from src.main.routes.api.empresa.empresa_response.find_all_empresa_response import FindAllEmpresaResponse
from src.main.routes.api.empresa.empresa_response.count_empresas_response import CountEmpresasResponse
from src.main.routes.api.empresas.empresas_response.find_all_empresas_with_pagination_response import FindAllEmpresasWithPaginationResponse
from src.main.routes.api.__error.error_response import generate_error_responses

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/empresa'
TAGS = ['empresas']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{empresa_name}', response_model=FindEmpresaResponse, responses=generate_error_responses())
async def find_empresa(empresa_name, request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    """
    Endpoint para buscar uma empresa específica pelo nome exato.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        empresa_name: Nome exato da empresa a ser buscada
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindEmpresaResponse: Dados da empresa encontrada
        
    Raises:
        EmpresaNotFoundError: Se a empresa não for encontrada
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['empresa_name'] = empresa_name
        http_response = await request_adapter(request, find_empresa_by_exact_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/all', response_model=FindAllEmpresaResponse, responses=generate_error_responses())
async def find_all_empresa(request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as empresas do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllEmpresaResponse: Lista com todas as empresas do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_empresas_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.get('/count/all', response_model=CountEmpresasResponse, responses=generate_error_responses())
async def count_empresas(request:Request, user=Security(role_required(["VEREADOR", "ADMIN", "ASSESSOR"]))):
    """
    Endpoint para contar o total de empresas no sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        CountEmpresasResponse: Número total de empresas
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, count_empresas_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_empresa(body:CreateEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar uma nova empresa no sistema.
    Apenas usuários ADMIN podem criar empresas.
    
    Args:
        body: Dados da empresa a ser criada (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        EmpresaAlreadyExistsError: Se a empresa já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.delete('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_empresa(body:DeleteEmpresaFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar uma empresa do sistema.
    Apenas usuários ADMIN podem deletar empresas.
    
    Args:
        body: Dados da empresa a ser deletada (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        EmpresaNotFoundError: Se a empresa não for encontrada
        EmpresaHasRelatedChildrenError: Se a empresa possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_empresa_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.patch('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_empresa(body:UpdateEmpresasFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o nome de uma empresa.
    Apenas usuários ADMIN podem alterar nomes de empresas.
    
    Args:
        body: Dados para atualização (nome atual e novo nome da empresa)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        EmpresaNotFoundError: Se a empresa não for encontrada
        EmpresaAlreadyExistsError: Se já existir uma empresa com o novo nome
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_empresas_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=http_response,
            request=request
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)

@routes.get("/pagination/{page_size}/{page}", response_model=FindAllEmpresasWithPaginationResponse, responses=generate_error_responses())
async def find_all_empresas_with_pagination(page_size:int, page:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as empresas com paginação.
    Retorna uma lista paginada de empresas para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de empresas por página
        page: Número da página (começa em 1)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllEmpresasWithPaginationResponse: Lista paginada de empresas com metadados de paginação
        
    Raises:
        InvalidPaginationError: Se os parâmetros de paginação forem inválidos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params["page_size"] = page_size
        request.path_params["page"] = page
        http_response = await request_adapter(request, find_all_empresas_with_pagination_composer())
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

@routes.get("/pagination-filter/{page_size}/{page}", response_model=FindAllEmpresasWithPaginationResponse, responses=generate_error_responses())
async def find_all_empresas_with_pagination_and_filter(page_size:int, page:int, request:Request, search: str = None, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as empresas com paginação e filtro global.
    Retorna uma lista paginada de empresas filtradas para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de empresas por página
        page: Número da página (começa em 1)
        search: Termo de busca opcional para filtrar empresas
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllEmpresasWithPaginationResponse: Lista paginada de empresas com metadados de paginação
        
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
                'search': search
            },
            path_params={
                'page_size': page_size,
                'page': page
            },
            url=str(request.url)
        )
        
        # Processar requisição
        http_response = find_all_empresas_with_pagination_and_filter_composer()(http_request)
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
