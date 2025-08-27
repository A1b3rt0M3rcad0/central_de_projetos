#pylint:disable=W0718,W9016
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.adapters.generic_cache_aside_adapter import simple_cache_aside_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_bairro_by_name_composer import find_bairro_by_name_composer
from src.main.composers.create_bairro_composer import create_bairro_composer
from src.main.composers.delete_bairro_composer import delete_bairro_composer
from src.main.composers.update_bairro_name_composer import update_bairro_name_composer
from src.main.composers.find_all_bairro_composer import find_all_bairro_composer
from src.main.composers.count_bairros_composer import count_bairros_composer

# Cache composers
from src.main.composers.cache.bairro.get.get_bairro_by_name_cached_composer import get_bairro_by_name_cached_composer
from src.main.composers.cache.bairro.set.set_bairro_by_name_cached_composer import set_bairro_by_name_cached_composer
from src.main.composers.cache.bairro.get.get_count_bairros_cached_composer import get_count_bairros_cached_composer
from src.main.composers.cache.bairro.set.set_count_bairros_cached_composer import set_count_bairros_cached_composer
from src.main.composers.cache.bairro.get.get_all_bairros_cached_composer import get_all_bairros_cached_composer
from src.main.composers.cache.bairro.set.set_all_bairros_cached_composer import set_all_bairros_cached_composer

from src.main.routes.api.__error.error_response import generate_error_responses

from src.main.routes.api.bairro.request_format.create_bairro_format import CreateBairroFormat
from src.main.routes.api.bairro.request_format.delete_bairro_format import DeleteBairroFormat
from src.main.routes.api.bairro.request_format.update_bairro_name_format import UpdateBairroNameFormat

from src.main.routes.api.bairro.bairro_response.find_bairro_by_name_response import FindBairroByNameResponse
from src.main.routes.api.bairro.bairro_response.count_bairros_response import CountBairrosResponse
from src.main.routes.api.bairro.bairro_response.find_all_bairro_response import FindAllBairroResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

## Logs
from src.logs.log_http import log_http

PREFIX = '/bairro'
TAGS = ['bairros']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{bairro_name}', response_model=FindBairroByNameResponse, responses=generate_error_responses())
async def find_bairro_by_name(bairro_name:str, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar um bairro específico pelo nome.
    Implementa cache-aside: primeiro busca no Redis, se não encontrar busca no banco.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        bairro_name: Nome do bairro a ser buscado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindBairroByNameResponse: Dados do bairro encontrado
        
    Raises:
        BairroNotFoundError: Se o bairro não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        # Usa o cache-aside adapter para implementar o padrão cache
        http_response = await simple_cache_aside_adapter(
            framework_request=request,
            cache_get_controller=get_bairro_by_name_cached_composer(),
            db_controller=find_bairro_by_name_composer(),
            cache_set_controller=set_bairro_by_name_cached_composer(),
            cache_key='bairro_name'
        )
        
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            http_response=http_response,
            level='INFO',
            logger_name=PREFIX,
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

@routes.get('/count/all', response_model=CountBairrosResponse, responses=generate_error_responses())
async def count_bairros(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para contar o total de bairros no sistema.
    Implementa cache-aside: primeiro busca no Redis, se não encontrar busca no banco.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        CountBairrosResponse: Número total de bairros
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        # Usa o cache-aside adapter para implementar o padrão cache
        http_response = await simple_cache_aside_adapter(
            framework_request=request,
            cache_get_controller=get_count_bairros_cached_composer(),
            db_controller=count_bairros_composer(),
            cache_set_controller=set_count_bairros_cached_composer(),
            cache_key='count_bairros'
        )
        
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            logger_name=PREFIX,
            level='INFO',
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)

    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get('/bairro/all', response_model=FindAllBairroResponse, responses=generate_error_responses())
async def find_all_bairro(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os bairros do sistema.
    Implementa cache-aside: primeiro busca no Redis, se não encontrar busca no banco.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllBairroResponse: Lista com todos os bairros do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        # Usa o cache-aside adapter para implementar o padrão cache
        http_response = await simple_cache_aside_adapter(
            framework_request=request,
            cache_get_controller=get_all_bairros_cached_composer(),
            db_controller=find_all_bairro_composer(),
            cache_set_controller=set_all_bairros_cached_composer(),
            cache_key='all_bairros'
        )
        
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            request=request,
            logger_name=PREFIX,
            http_response=http_response
        )
        return response_adapter(http_response)

    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_bairro(body:CreateBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar um novo bairro no sistema.
    Apenas usuários ADMIN podem criar bairros.
    
    Args:
        body: Dados do bairro a ser criado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        BairroAlreadyExistsError: Se o bairro já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_bairro_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.delete('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_bairro(body:DeleteBairroFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar um bairro do sistema.
    Apenas usuários ADMIN podem deletar bairros.
    
    Args:
        body: Dados do bairro a ser deletado (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        BairroNotFoundError: Se o bairro não for encontrado
        BairroHasRelatedChildrenError: Se o bairro possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_bairro_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response)
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.patch('/name', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_bairro_name(body:UpdateBairroNameFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o nome de um bairro.
    Apenas usuários ADMIN podem alterar nomes de bairros.
    
    Args:
        body: Dados para atualização (nome atual e novo nome do bairro)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        BairroNotFoundError: Se o bairro não for encontrado
        BairroAlreadyExistsError: Se já existir um bairro com o novo nome
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_bairro_name_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            logger_name=PREFIX,
            request=request,
            http_response=http_response
        )
        return response_adapter(http_response) 
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)