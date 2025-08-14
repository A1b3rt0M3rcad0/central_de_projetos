#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

## Composers
from src.main.composers.create_project_fiscal_composer import create_project_fiscal_composer
from src.main.composers.delete_project_fiscal_composer import delete_project_fiscal_composer
from src.main.composers.get_count_projects_by_fiscal_composer import get_count_projects_by_fiscal_composer

## request Formats
from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project_fiscal.request_format.create_project_fiscal import CreateProjectFiscalFormat
from src.main.routes.api.project_fiscal.request_format.delete_project_fiscal import DeleteProjectFiscalFormat
from src.main.routes.api.project_fiscal.project_fiscal_response.get_count_projects_by_fiscal_response import GetCountProjectsByFiscalResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/project_fiscal'
TAGS = ['project', 'fiscal', 'project_fiscal']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post("/", response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_project_fiscal(body:CreateProjectFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar uma nova associação entre projeto e fiscal.
    Vincula um projeto a um fiscal responsável.
    Apenas usuários ADMIN podem criar associações.
    
    Args:
        body: Dados da associação (project_id e fiscal_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        FiscalNotFoundError: Se o fiscal não for encontrado
        AssociationAlreadyExistsError: Se a associação já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_project_fiscal_composer())
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

@routes.get("/project/count", response_model=GetCountProjectsByFiscalResponse, responses=generate_error_responses())
async def get_count_projects_by_fiscal(request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para obter contagem de projetos agrupados por fiscal.
    Retorna estatísticas de quantos projetos cada fiscal supervisiona.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetCountProjectsByFiscalResponse: Lista com contagem de projetos por fiscal
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, get_count_projects_by_fiscal_composer())
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

@routes.delete("/", response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_project_fiscal(body:DeleteProjectFiscalFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar uma associação entre projeto e fiscal.
    Remove o vínculo entre um projeto e um fiscal.
    Apenas usuários ADMIN podem deletar associações.
    
    Args:
        body: Dados da associação a ser removida (project_id e fiscal_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        FiscalNotFoundError: Se o fiscal não for encontrado
        AssociationNotFoundError: Se a associação não existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_project_fiscal_composer())
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