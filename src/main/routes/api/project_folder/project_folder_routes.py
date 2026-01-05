#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_project_folder_composer import find_project_folder_composer
from src.main.composers.create_project_folder_composer import create_project_folder_composer
from src.main.composers.delete_project_folder_composer import delete_project_folder_composer
from src.main.composers.find_all_projects_from_folder_composer import find_all_projects_from_folder_composer
from src.main.composers.find_all_folders_from_project_composer import find_all_folders_from_project_composer
from src.main.composers.delete_all_projects_from_folder_composer import delete_all_projects_from_folder_composer

from src.main.routes.api.project_folder.request_format.create_project_folder_format import CreateProjectFolderFormat
from src.main.routes.api.project_folder.request_format.delete_project_folder_format import DeleteProjectFolderFormat

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.project_folder.project_folder_response.find_project_folder_response import FindProjectFolderResponse
from src.main.routes.api.project_folder.project_folder_response.find_all_projects_from_folder_response import FindAllProjectsFromFolderResponse
from src.main.routes.api.project_folder.project_folder_response.find_all_folders_from_project_response import FindAllFoldersFromProjectResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http

PREFIX = '/project_folder'
TAGS = ['project', 'folder']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/folder/{folder_id}', response_model=FindAllProjectsFromFolderResponse, responses=generate_error_responses())
async def find_all_projects_from_folder(folder_id: int, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todos os projetos associados a uma pasta específica.
    Retorna lista de todos os projetos que estão vinculados à pasta.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        folder_id: ID da pasta
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllProjectsFromFolderResponse: Lista de projetos da pasta
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['folder_id'] = folder_id
        http_response = await request_adapter(request, find_all_projects_from_folder_composer())
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

@routes.get('/project/{project_id}', response_model=FindAllFoldersFromProjectResponse, responses=generate_error_responses())
async def find_all_folders_from_project(project_id: int, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as pastas associadas a um projeto específico.
    Retorna lista de todas as pastas que estão vinculadas ao projeto.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        project_id: ID do projeto
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFoldersFromProjectResponse: Lista de pastas do projeto
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, find_all_folders_from_project_composer())
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

@routes.get('/{project_id}/{folder_id}', response_model=FindProjectFolderResponse, responses=generate_error_responses())
async def find_project_folder(project_id: int, folder_id: int, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar uma associação específica entre projeto e pasta.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        project_id: ID do projeto
        folder_id: ID da pasta
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindProjectFolderResponse: Dados da associação projeto-pasta
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        FolderNotFoundError: Se a pasta não for encontrada
        AssociationNotFoundError: Se a associação não existir
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        request.path_params['folder_id'] = folder_id
        http_response = await request_adapter(request, find_project_folder_composer())
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
async def create_project_folder(body: CreateProjectFolderFormat, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar uma nova associação entre projeto e pasta.
    Vincula um projeto a uma pasta específica.
    Apenas usuários ADMIN podem criar associações.
    
    Args:
        body: Dados da associação (project_id e folder_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        FolderNotFoundError: Se a pasta não for encontrada
        AssociationAlreadyExistsError: Se a associação já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_project_folder_composer())
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
async def delete_project_folder(body: DeleteProjectFolderFormat, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar uma associação entre projeto e pasta.
    Remove o vínculo entre um projeto e uma pasta.
    Apenas usuários ADMIN podem deletar associações.
    
    Args:
        body: Dados da associação a ser removida (project_id e folder_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        FolderNotFoundError: Se a pasta não for encontrada
        AssociationNotFoundError: Se a associação não existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_project_folder_composer())
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

@routes.delete('/folder/{folder_id}', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_all_projects_from_folder(folder_id: int, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar todas as associações de projetos de uma pasta.
    Remove todos os vínculos entre projetos e uma pasta específica.
    Apenas usuários ADMIN podem deletar associações.
    
    Args:
        folder_id: ID da pasta
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['folder_id'] = folder_id
        http_response = await request_adapter(request, delete_all_projects_from_folder_composer())
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

