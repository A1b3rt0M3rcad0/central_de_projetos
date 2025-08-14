#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_project_type_composer import create_project_type_composer
from src.main.composers.find_type_from_project_composer import find_type_from_project_composer
from src.main.composers.delete_project_type_composer import delete_project_type_composer
from src.main.composers.get_project_types_count_by_bairro_composer import get_project_types_count_by_bairro_composer

from src.main.routes.api.project_type.request_format.create_project_type_format import CreateProjectTypeFormat
from src.main.routes.api.project_type.request_format.delete_project_type_format import DeleteProjectTypeFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project_type.project_type_response.find_type_from_project_response import FindTypeFromProjectResponse
from src.main.routes.api.project_type.project_type_response.get_project_types_count_by_bairro import GetProjectTypesCountByBairroResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/project_type'
TAGS = ['project', 'type']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/{project_id}', response_model=FindTypeFromProjectResponse, responses=generate_error_responses())
async def find_type_from_project(project_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar o tipo de um projeto específico.
    Retorna informações sobre o tipo/categoria do projeto.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        project_id: ID do projeto
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindTypeFromProjectResponse: Dados do tipo do projeto
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        TypeNotFoundError: Se o tipo não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_type_from_project_composer())
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

@routes.get('/project/types/count', response_model=GetProjectTypesCountByBairroResponse, responses=generate_error_responses())
async def get_project_types_count_by_bairro(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para obter contagem de tipos de projetos agrupados por bairro.
    Retorna estatísticas de tipos de projeto por bairro (infraestrutura, educação, etc.).
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetProjectTypesCountByBairroResponse: Lista com contagem de tipos por bairro
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, get_project_types_count_by_bairro_composer())
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
async def create_project_type(body:CreateProjectTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar uma nova associação entre projeto e tipo.
    Vincula um projeto a um tipo/categoria específica.
    Apenas usuários ADMIN podem criar associações.
    
    Args:
        body: Dados da associação (project_id e type_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        TypeNotFoundError: Se o tipo não for encontrado
        AssociationAlreadyExistsError: Se a associação já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response  = await request_adapter(request, create_project_type_composer())
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
async def delete_project_type(body:DeleteProjectTypeFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar uma associação entre projeto e tipo.
    Remove o vínculo entre um projeto e um tipo/categoria.
    Apenas usuários ADMIN podem deletar associações.
    
    Args:
        body: Dados da associação a ser removida (project_id e type_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        TypeNotFoundError: Se o tipo não for encontrado
        AssociationNotFoundError: Se a associação não existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_project_type_composer())
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