#pylint:disable=W0718
#pylint:disable=W0613
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

from src.main.routes.api.status.format_request.create_status_format import CreateStatusFormat
from src.main.routes.api.status.format_request.delete_status_format import DeleteStatusFormat
from src.main.routes.api.status.format_request.update_status_description_format import UpdateStatusDescriptionFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.status.status_response.find_status_response import FindStatusReponse
from src.main.routes.api.status.status_response.find_all_status_response import FindAllStatusResponse
from src.main.routes.api.status.status_response.find_project_by_status_response import FindProjectbyStatusReponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/status'
TAGS = ['status']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

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
    Apenas usuários ADMIN podem criar status.
    
    Args:
        body: Dados do status a ser criado (descrição)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        StatusAlreadyExistsError: Se o status já existir
        UnauthorizedError: Se o usuário não for ADMIN
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
    Endpoint para deletar um status do sistema.
    Apenas usuários ADMIN podem deletar status.
    
    Args:
        body: Dados do status a ser deletado (ID)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        StatusHasRelatedChildrenError: Se o status possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
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
    Endpoint para atualizar a descrição de um status.
    Apenas usuários ADMIN podem alterar descrições de status.
    
    Args:
        body: Dados para atualização (ID do status e nova descrição)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        StatusNotFoundError: Se o status não for encontrado
        StatusAlreadyExistsError: Se já existir um status com a nova descrição
        UnauthorizedError: Se o usuário não for ADMIN
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
    
@routes.get('/status/all/', response_model=FindAllStatusResponse, responses=generate_error_responses())
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