#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter, UploadFile, File, Form
from fastapi import Request
from typing import List
from src.main.adapters.multipart_adapter import multipart_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.adapters.request_adapter import request_adapter
from src.errors.error_handle import error_handler
from src.presentation.http_types.http_request import HttpRequest

from src.main.composers.create_work_project_with_fiscal_document_composer import create_work_project_with_fiscal_document_composer
from src.main.composers.add_documents_to_work_project_composer import add_documents_to_work_project_composer
from src.main.composers.delete_work_project_composer import delete_work_project_composer
from src.main.composers.get_work_project_composer import get_work_project_composer
from src.main.composers.get_work_projects_with_pagination_composer import get_work_projects_by_project_with_pagination_composer

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.work_project.work_project_response.create_work_project_with_fiscal_document_response import CreateWorkProjectWithFiscalDocumentResponse
from src.main.routes.api.work_project.work_project_response.add_documents_to_work_project_response import AddDocumentsToWorkProjectResponse
from src.main.routes.api.work_project.work_project_response.delete_work_project_response import DeleteWorkProjectResponse
from src.main.routes.api.work_project.work_project_response.get_work_project_response import GetWorkProjectResponse
from src.main.routes.api.work_project.work_project_response.get_work_projects_with_pagination_response import GetWorkProjectsByProjectWithPaginationResponse

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logger
from src.logs.log_http import log_http

PREFIX = '/work_project'
TAGS = ['work_project']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post('/create_with_fiscal_documents', response_model=CreateWorkProjectWithFiscalDocumentResponse, responses=generate_error_responses())
async def create_work_project_with_fiscal_documents(
    request: Request,
    project_id: int = Form(...),
    fiscal_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(None),
    user: dict = Security(role_required(["ADMIN"]))
):
    try:
        # Preparar dados do formulário
        form_data = {
            'project_id': project_id,
            'fiscal_id': fiscal_id,
            'title': title,
            'description': description
        }
        
        # Usar multipart_adapter para processar formulário + arquivos
        http_response = await multipart_adapter(
            request=request,
            controller=create_work_project_with_fiscal_document_composer(),
            form_data=form_data,
            files=files
        )
        
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


@routes.post('/add_documents', response_model=AddDocumentsToWorkProjectResponse, responses=generate_error_responses())
async def add_documents_to_work_project(
    request: Request,
    work_project_id: int = Form(...),
    files: List[UploadFile] = File(None),
    user: dict = Security(role_required(["ADMIN"]))
):
    """
    Endpoint para adicionar documentos a um work project.
    Apenas administradores podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project
        files: Lista de arquivos para adicionar
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        AddDocumentsToWorkProjectResponse: Mensagem de sucesso e lista de documentos adicionados
        
    Raises:
        WorkProjectNotExists: Se o work project não for encontrado
        InternalServerError: Para outros erros internos
    """
    try:
        # Preparar dados do formulário
        form_data = {
            'work_project_id': work_project_id
        }
        
        # Usar multipart_adapter para processar formulário + arquivos
        http_response = await multipart_adapter(
            request=request,
            controller=add_documents_to_work_project_composer(),
            form_data=form_data,
            files=files
        )
        
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


@routes.get('/{work_project_id}', response_model=GetWorkProjectResponse, responses=generate_error_responses())
async def get_work_project(
    request: Request,
    work_project_id: int,
    user: dict = Security(role_required(["ADMIN"]))
):
    """
    Endpoint para buscar um work project específico.
    Apenas administradores podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project a ser buscado
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetWorkProjectResponse: Dados do work project encontrado
        
    Raises:
        WorkProjectNotExists: Se o work project não for encontrado
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['work_project_id'] = work_project_id
        http_response = await request_adapter(request, get_work_project_composer())
        
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


@routes.get('/project/{project_id}/pagination/{page_size}/{page}', response_model=GetWorkProjectsByProjectWithPaginationResponse, responses=generate_error_responses())
async def get_work_projects_by_project_with_pagination(
    request: Request,
    project_id: int,
    page_size: int,
    page: int,
    user: dict = Security(role_required(["ADMIN"]))
):
    """
    Endpoint para buscar work projects de um projeto específico com paginação.
    Apenas administradores podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        project_id: ID do projeto
        page_size: Número de itens por página
        page: Número da página
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetWorkProjectsByProjectWithPaginationResponse: Lista de work projects do projeto com informações de paginação
        
    Raises:
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        request.path_params['page'] = page
        request.path_params['page_size'] = page_size
        http_response = await request_adapter(request, get_work_projects_by_project_with_pagination_composer())
        
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


@routes.delete('/{work_project_id}', response_model=DeleteWorkProjectResponse, responses=generate_error_responses())
async def delete_work_project(
    request: Request,
    work_project_id: int,
    user: dict = Security(role_required(["ADMIN"]))
):
    """
    Endpoint para deletar um work project e todos os seus documentos relacionados.
    Apenas administradores podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project a ser deletado
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        DeleteWorkProjectResponse: Mensagem de sucesso e ID do work project deletado
        
    Raises:
        WorkProjectNotExists: Se o work project não for encontrado
        DeleteWorkProjectError: Se houver erro na deleção
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = delete_work_project_composer()(
            HttpRequest(
                path_params={'work_project_id': work_project_id}
            )
        )
        
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