#pylint:disable=W0718
#pylint:disable=W0613,W0012,W9016
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_fiscal_by_name_composer import find_fiscal_by_name_composer
from src.main.composers.create_fiscal_composer import create_fiscal_composer
from src.main.composers.delete_fiscal_composer import delete_fiscal_composer
from src.main.composers.update_fiscal_name_composer import update_fiscal_name_composer
from src.main.composers.find_all_fiscal_composer import find_all_fiscal_composer
from src.main.composers.count_fiscals_composer import count_fiscals_composer
from src.main.composers.insert_all_fiscal_from_user_composer import insert_all_fiscal_from_user_composer
from src.main.composers.find_all_fiscais_with_pagination_composer import find_all_fiscais_with_pagination_composer
from src.main.composers.find_all_fiscais_with_pagination_and_filter_composer import find_all_fiscais_with_pagination_and_filter_composer

from src.main.routes.api.fiscal.request_format.create_fiscal_format import CreateFiscalFormat
from src.main.routes.api.fiscal.request_format.delete_fiscal_format import DeleteFiscalFormat
from src.main.routes.api.fiscal.request_format.update_fiscal_name_format import UpdateFiscalNameFormat
from src.main.routes.api.fiscal.request_format.insert_all_fiscal_from_user_format import InsertAllFiscalFromUserFormat
from src.main.routes.api.fiscal.fiscal_response.find_fiscal_by_name_response import FindFiscalByNameResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.fiscal.fiscal_response.find_all_fiscal_response import FindAllFiscalReponse
from src.main.routes.api.fiscal.fiscal_response.count_fiscal_response import CountFiscalReponse
from src.main.routes.api.fiscais.fiscais_response.find_all_fiscais_with_pagination_response import FindAllFiscaisWithPaginationResponse
from src.main.routes.api.__error.error_response import generate_error_responses

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/fiscal'
TAGS = ['fiscal']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{fiscal_name}', response_model=FindFiscalByNameResponse, responses=generate_error_responses())
async def find_fiscal_by_name(fiscal_name, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar um fiscal específico pelo nome.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        fiscal_name: Nome do fiscal a ser buscado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindFiscalByNameResponse: Dados do fiscal encontrado
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['fiscal_name'] = fiscal_name
        http_response = await request_adapter(request, find_fiscal_by_name_composer())
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

@routes.get('/fiscal/all', response_model=FindAllFiscalReponse, responses=generate_error_responses())
async def find_all_fiscal(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os fiscais do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFiscalResponse: Lista com todos os fiscais do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_all_fiscal_composer())
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

@routes.get('/fiscal/count/all', response_model=CountFiscalReponse, responses=generate_error_responses())
async def count_fiscals(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para contar o total de fiscais no sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        CountFiscalResponse: Número total de fiscais
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, count_fiscals_composer())
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
async def create_fiscal(body:CreateFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar um novo fiscal no sistema.
    Apenas usuários ADMIN podem criar fiscais.
    
    Args:
        body: Dados do fiscal a ser criado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        FiscalAlreadyExistsError: Se o fiscal já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_fiscal_composer())
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
async def delete_fiscal(body:DeleteFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar um fiscal do sistema.
    Apenas usuários ADMIN podem deletar fiscais.
    
    Args:
        body: Dados do fiscal a ser deletado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        FiscalHasRelatedChildrenError: Se o fiscal possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_fiscal_composer())
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
async def update_fiscal(body:UpdateFiscalNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o nome de um fiscal.
    Apenas usuários ADMIN podem alterar nomes de fiscais.
    
    Args:
        body: Dados para atualização (nome atual e novo nome do fiscal)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        FiscalAlreadyExistsError: Se já existir um fiscal com o novo nome
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_fiscal_name_composer())
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

@routes.post('/insert-all', response_model=BaseMessageResponse, responses=generate_error_responses())
async def insert_all_fiscal_from_user(body:InsertAllFiscalFromUserFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para inserir fiscal com todos os dados (nome, email, senha, telefone).
    Apenas ADMIN pode acessar este endpoint.
    
    Args:
        body: Dados do fiscal (nome, email, senha, telefone)
        request: Objeto da requisição HTTP
        user: Usuário autenticado (deve ser ADMIN)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso
        
    Raises:
        FiscalAlreadyExists: Se o fiscal já existe
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, insert_all_fiscal_from_user_composer())
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

@routes.get("/fiscal/pagination/{page_size}/{page}", response_model=FindAllFiscaisWithPaginationResponse, responses=generate_error_responses())
async def find_all_fiscais_with_pagination(page_size:int, page:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os fiscais com paginação.
    Retorna uma lista paginada de fiscais para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de fiscais por página
        page: Número da página (começa em 1)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFiscaisWithPaginationResponse: Lista paginada de fiscais com metadados de paginação
        
    Raises:
        InvalidPaginationError: Se os parâmetros de paginação forem inválidos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params["page_size"] = page_size
        request.path_params["page"] = page
        http_response = await request_adapter(request, find_all_fiscais_with_pagination_composer())
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

@routes.get("/fiscais/pagination-filter/{page_size}/{page}", response_model=FindAllFiscaisWithPaginationResponse, responses=generate_error_responses())
async def find_all_fiscais_with_pagination_and_filter(page_size:int, page:int, request:Request, search: str = None, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os fiscais com paginação e filtro global.
    Retorna uma lista paginada de fiscais filtrados para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de fiscais por página
        page: Número da página (começa em 1)
        search: Termo de busca opcional para filtrar fiscais
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFiscaisWithPaginationResponse: Lista paginada de fiscais com metadados de paginação
        
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
        http_response = find_all_fiscais_with_pagination_and_filter_composer()(http_request)
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
