#pylint:disable=W0718,W9016
#pylint:disable=W0613
from fastapi import APIRouter
from fastapi import Request
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.find_folder_by_id_composer import find_folder_by_id_composer
from src.main.composers.find_folder_by_name_composer import find_folder_by_name_composer
from src.main.composers.create_folder_composer import create_folder_composer
from src.main.composers.delete_folder_composer import delete_folder_composer
from src.main.composers.update_folder_composer import update_folder_composer
from src.main.composers.find_all_folder_composer import find_all_folder_composer
from src.main.composers.count_folders_composer import count_folders_composer
from src.main.composers.find_all_folders_with_pagination_composer import find_all_folders_with_pagination_composer
from src.main.composers.find_all_folders_with_pagination_and_filter_composer import find_all_folders_with_pagination_and_filter_composer

from src.main.routes.api.__error.error_response import generate_error_responses

from src.main.routes.api.folder.request_format.create_folder_format import CreateFolderFormat
from src.main.routes.api.folder.request_format.delete_folder_format import DeleteFolderFormat
from src.main.routes.api.folder.request_format.update_folder_format import UpdateFolderFormat

from src.main.routes.api.folder.folder_response.find_folder_by_id_response import FindFolderByIdResponse
from src.main.routes.api.folder.folder_response.find_folder_by_name_response import FindFolderByNameResponse
from src.main.routes.api.folder.folder_response.count_folders_response import CountFoldersResponse
from src.main.routes.api.folder.folder_response.find_all_folder_response import FindAllFolderResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.folder.folder_response.find_all_folders_with_pagination_response import FindAllFoldersWithPaginationResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

## Logs
from src.logs.log_http import log_http

PREFIX = '/folder'
TAGS = ['folders']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.get('/all', response_model=FindAllFolderResponse, responses=generate_error_responses())
async def find_all_folder(request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as pastas do sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFolderResponse: Lista com todas as pastas do sistema
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, find_all_folder_composer())
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

@routes.get('/count/all', response_model=CountFoldersResponse, responses=generate_error_responses())
async def count_folders(request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para contar o total de pastas no sistema.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        CountFoldersResponse: Número total de pastas
        
    Raises:
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, count_folders_composer())
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

@routes.get('/name/{folder_name}', response_model=FindFolderByNameResponse, responses=generate_error_responses())
async def find_folder_by_name(folder_name: str, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar uma pasta específica pelo nome.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        folder_name: Nome da pasta a ser buscada
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindFolderByNameResponse: Dados da pasta encontrada
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['folder_name'] = folder_name
        http_response = await request_adapter(request, find_folder_by_name_composer())
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

@routes.get('/{folder_id}', response_model=FindFolderByIdResponse, responses=generate_error_responses())
async def find_folder_by_id(folder_id: int, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar uma pasta específica pelo ID.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        folder_id: ID da pasta a ser buscada
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindFolderByIdResponse: Dados da pasta encontrada
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['folder_id'] = folder_id
        http_response = await request_adapter(request, find_folder_by_id_composer())
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

@routes.post('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def create_folder(body: CreateFolderFormat, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para criar uma nova pasta no sistema.
    Apenas usuários ADMIN podem criar pastas.
    
    Args:
        body: Dados da pasta a ser criada (nome)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na criação
        
    Raises:
        FolderAlreadyExistsError: Se a pasta já existir
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, create_folder_composer())
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
async def delete_folder(body: DeleteFolderFormat, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar uma pasta do sistema.
    Apenas usuários ADMIN podem deletar pastas.
    
    Args:
        body: Dados da pasta a ser deletada (folder_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        FolderHasRelatedChildrenError: Se a pasta possui relacionamentos que impedem a deleção
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_folder_composer())
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

@routes.patch('/', response_model=BaseMessageResponse, responses=generate_error_responses())
async def update_folder(body: UpdateFolderFormat, request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para atualizar o nome de uma pasta.
    Apenas usuários ADMIN podem alterar nomes de pastas.
    
    Args:
        body: Dados para atualização (folder_id e new_name)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na atualização
        
    Raises:
        FolderNotFoundError: Se a pasta não for encontrada
        FolderAlreadyExistsError: Se já existir uma pasta com o novo nome
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, update_folder_composer())
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

@routes.get("/pagination/{page_size}/{page}", response_model=FindAllFoldersWithPaginationResponse, responses=generate_error_responses())
async def find_all_folders_with_pagination(page_size: int, page: int, request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as pastas com paginação.
    Retorna uma lista paginada de pastas para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de pastas por página
        page: Número da página (começa em 1)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFoldersWithPaginationResponse: Lista paginada de pastas com metadados de paginação
        
    Raises:
        InvalidPaginationError: Se os parâmetros de paginação forem inválidos
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params["page_size"] = page_size
        request.path_params["page"] = page
        http_response = await request_adapter(request, find_all_folders_with_pagination_composer())
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

@routes.get("/pagination-filter/{page_size}/{page}", response_model=FindAllFoldersWithPaginationResponse, responses=generate_error_responses())
async def find_all_folders_with_pagination_and_filter(page_size: int, page: int, request: Request, search: str = None, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para buscar todas as pastas com paginação e filtro global.
    Retorna uma lista paginada de pastas filtradas para otimizar performance em grandes volumes.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        page_size: Número de pastas por página
        page: Número da página (começa em 1)
        search: Termo de busca opcional para filtrar pastas
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        FindAllFoldersWithPaginationResponse: Lista paginada de pastas com metadados de paginação
        
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
        http_response = find_all_folders_with_pagination_and_filter_composer()(http_request)
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

