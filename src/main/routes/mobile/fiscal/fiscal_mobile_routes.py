#pylint:disable=W0611, W0613
from fastapi import APIRouter, Request, Security, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime
from src.errors.error_handle import error_handler
from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.middleware.fiscal_authorization import fiscal_required
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.multipart_adapter import multipart_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.composers.login_fiscal_composer import login_fiscal_composer
from src.main.composers.add_documents_to_work_project_mobile_composer import add_documents_to_work_project_mobile_composer
from src.main.composers.create_work_project_mobile_composer import create_work_project_mobile_composer
from src.main.composers.delete_work_project_mobile_composer import delete_work_project_mobile_composer
from src.main.composers.get_work_projects_by_fiscal_mobile_composer import get_work_projects_by_fiscal_mobile_composer
from src.main.composers.get_latest_work_projects_by_fiscal_composer import get_latest_work_projects_by_fiscal_composer
from src.main.composers.get_work_project_by_fiscal_mobile_composer import get_work_project_by_fiscal_mobile_composer
from src.main.composers.get_projects_by_fiscal_with_pagination_composer import get_projects_by_fiscal_with_pagination_composer
from src.main.routes.mobile.fiscal.request_format.login_fiscal_format import LoginFiscalFormat
from src.main.routes.mobile.fiscal.response_format.login_fiscal_response import LoginFiscalResponse
from src.main.routes.mobile.fiscal.response_format.test_fiscal_response import FiscalTestResponse
from src.main.routes.mobile.fiscal.response_format.add_documents_to_work_project_response import AddDocumentsToWorkProjectMobileResponse
from src.main.routes.mobile.fiscal.response_format.create_work_project_response import CreateWorkProjectMobileResponse
from src.main.routes.mobile.fiscal.response_format.delete_work_project_response import DeleteWorkProjectMobileResponse
from src.main.routes.mobile.fiscal.response_format.get_work_projects_by_fiscal_response import GetWorkProjectsByFiscalMobileResponse
from src.main.routes.mobile.fiscal.response_format.get_latest_work_projects_by_fiscal_response import GetLatestWorkProjectsByFiscalResponse
from src.main.routes.mobile.fiscal.response_format.get_work_project_by_fiscal_response import GetWorkProjectByFiscalMobileResponse
from src.main.routes.mobile.fiscal.response_format.get_projects_by_fiscal_with_pagination_response import GetProjectsByFiscalWithPaginationMobileResponse
from src.logs.log_http import log_http
from src.presentation.http_types.http_response import HttpResponse

PREFIX = '/mobile/fiscal'

routes = APIRouter(prefix=PREFIX, tags=['Fiscal Mobile'])

@routes.post('/login', 
             response_model=LoginFiscalResponse, 
             responses=generate_error_responses())
async def login_fiscal_mobile(
    body: LoginFiscalFormat, 
    request: Request
):
    """
    Endpoint para login do fiscal via aplicativo mobile.
    
    Args:
        body: Dados de login (email e senha)
        request: Objeto da requisição HTTP
        
    Returns:
        LoginFiscalResponse: Token JWT e mensagem de sucesso
        
    Raises:
        FiscalNotFoundError: Se o fiscal não for encontrado
        InvalidPasswordError: Se a senha estiver incorreta
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, login_fiscal_composer())
        
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


@routes.post('/add_documents_to_work_project', 
             response_model=AddDocumentsToWorkProjectMobileResponse, 
             responses=generate_error_responses())
async def add_documents_to_work_project_mobile(
    request: Request,
    work_project_id: int = Form(...),
    files: List[UploadFile] = File(None),
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para adicionar documentos a um work project via aplicativo mobile.
    Apenas fiscais podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project
        files: Lista de arquivos para adicionar
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        AddDocumentsToWorkProjectMobileResponse: Mensagem de sucesso e lista de documentos adicionados
        
    Raises:
        WorkProjectNotExists: Se o work project não for encontrado
        InternalServerError: Para outros erros internos
    """
    try:
        # Preparar dados do formulário
        form_data = {
            'work_project_id': work_project_id
        }
        
        # Adicionar fiscal_id ao form_data para validação
        form_data['fiscal_id'] = fiscal.get('fiscal_id')
        
        # Usar multipart_adapter para processar formulário + arquivos
        http_response = await multipart_adapter(
            request=request,
            controller=add_documents_to_work_project_mobile_composer(),
            form_data=form_data,
            files=files
        )
        
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


@routes.post('/create_work_project', 
             response_model=CreateWorkProjectMobileResponse, 
             responses=generate_error_responses())
async def create_work_project_mobile(
    request: Request,
    project_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(None),
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para criar work project via aplicativo mobile.
    Apenas fiscais vinculados ao projeto podem criar work projects.
    
    Args:
        request: Objeto da requisição HTTP
        project_id: ID do projeto
        title: Título do work project
        description: Descrição do work project
        files: Lista de arquivos para adicionar
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        CreateWorkProjectMobileResponse: Dados do work project criado
        
    Raises:
        FiscalNotAuthorizedError: Se o fiscal não estiver vinculado ao projeto
        WorkProjectNotExists: Se o work project não for encontrado
        InternalServerError: Para outros erros internos
    """
    try:
        # Preparar dados do formulário
        form_data = {
            'project_id': project_id,
            'fiscal_id': fiscal.get('fiscal_id'),
            'title': title,
            'description': description
        }
        
        # Usar multipart_adapter para processar formulário + arquivos
        http_response = await multipart_adapter(
            request=request,
            controller=create_work_project_mobile_composer(),
            form_data=form_data,
            files=files
        )
        
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


@routes.delete('/delete_work_project/{work_project_id}', 
              response_model=DeleteWorkProjectMobileResponse, 
              responses=generate_error_responses())
async def delete_work_project_mobile(
    request: Request,
    work_project_id: int,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para deletar work project via aplicativo mobile.
    Apenas o fiscal associado ao work project pode deletá-lo.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project a ser deletado
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        DeleteWorkProjectMobileResponse: Mensagem de sucesso e dados do work project deletado
        
    Raises:
        WorkProjectNotExists: Se o work project não for encontrado
        FiscalNotAuthorizedError: Se o fiscal não estiver associado ao work project
        InternalServerError: Para outros erros internos
    """
    try:
        # Modificar o request para incluir o fiscal_id no body
        request.state.body = {
            'fiscal_id': fiscal.get('fiscal_id')
        }
        
        # Usar request_adapter para processar a requisição
        http_response = await request_adapter(
            request=request,
            controller=delete_work_project_mobile_composer()
        )
        
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


@routes.get('/work_projects/pagination/{project_id}/{page_size}/{page}', 
            response_model=GetWorkProjectsByFiscalMobileResponse, 
            responses=generate_error_responses())
async def get_work_projects_by_fiscal_mobile(
    request: Request,
    project_id: int,
    page_size: int,
    page: int,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para buscar work projects do fiscal autenticado por projeto específico com paginação via aplicativo mobile.
    Apenas fiscais podem acessar este endpoint e só veem seus próprios work projects.
    O fiscal só vê work projects de projetos onde ele está associado.
    
    Args:
        request: Objeto da requisição HTTP
        project_id: ID do projeto para filtrar os work projects
        page_size: Número de itens por página
        page: Número da página
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        GetWorkProjectsByFiscalMobileResponse: Lista de work projects do fiscal para o projeto específico com informações de paginação
        
    Raises:
        InternalServerError: Para outros erros internos
    """
    try:
        # Modificar o request para incluir o fiscal_id no body (padrão das outras rotas mobile)
        request.state.body = {
            'fiscal_id': fiscal.get('fiscal_id')
        }
        
        # Adicionar parâmetros de paginação ao path_params
        request.path_params['page'] = page
        request.path_params['page_size'] = page_size
        
        # Usar request_adapter para processar a requisição
        http_response = await request_adapter(
            request=request,
            controller=get_work_projects_by_fiscal_mobile_composer()
        )
        
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


@routes.get('/latest_work_projects/pagination/{page_size}/{page}', 
            response_model=GetLatestWorkProjectsByFiscalResponse, 
            responses=generate_error_responses())
async def get_latest_work_projects_by_fiscal(
    request: Request,
    page_size: int,
    page: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para buscar os últimos work projects do fiscal autenticado com paginação e filtro de data.
    Apenas fiscais podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        page_size: Tamanho da página
        page: Número da página
        start_date: Data de início para filtro (opcional, formato ISO: YYYY-MM-DDTHH:MM:SS)
        end_date: Data de fim para filtro (opcional, formato ISO: YYYY-MM-DDTHH:MM:SS)
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        GetLatestWorkProjectsByFiscalResponse: Lista de últimos work projects do fiscal ordenados por data de criação
        
    Raises:
        InternalServerError: Para outros erros internos
    """
    try:
        # Modificar o request para incluir o fiscal_id no body (padrão das outras rotas mobile)
        request.state.body = {
            'fiscal_id': fiscal.get('fiscal_id')
        }
        
        # Usar request_adapter para processar a requisição
        http_response = await request_adapter(
            request=request,
            controller=get_latest_work_projects_by_fiscal_composer()
        )
        
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


@routes.get('/work_project/{work_project_id}', 
            response_model=GetWorkProjectByFiscalMobileResponse, 
            responses=generate_error_responses())
async def get_work_project_by_fiscal_mobile(
    request: Request,
    work_project_id: int,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para buscar um work project específico verificando se o fiscal está associado.
    Apenas fiscais podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        work_project_id: ID do work project
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        GetWorkProjectByFiscalMobileResponse: Dados do work project se o fiscal estiver associado
        
    Raises:
        WorkProjectNotExists: Se o work project não existir ou o fiscal não estiver associado
        InternalServerError: Para outros erros internos
    """
    try:
        # Modificar o request para incluir o work_project_id e fiscal_id no body
        request.state.body = {
            'work_project_id': work_project_id,
            'fiscal_id': fiscal.get('fiscal_id')
        }
        
        # Usar request_adapter para processar a requisição
        http_response = await request_adapter(
            request=request,
            controller=get_work_project_by_fiscal_mobile_composer()
        )
        
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


@routes.get('/projects/pagination/{page_size}/{page}', 
            response_model=GetProjectsByFiscalWithPaginationMobileResponse, 
            responses=generate_error_responses())
async def get_projects_by_fiscal_with_pagination_mobile(
    request: Request,
    page_size: int,
    page: int,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint para buscar todos os projetos associados ao fiscal com paginação.
    Apenas fiscais podem acessar este endpoint.
    
    Args:
        request: Objeto da requisição HTTP
        page_size: Tamanho da página
        page: Número da página
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        GetProjectsByFiscalWithPaginationMobileResponse: Lista paginada de projetos associados ao fiscal
        
    Raises:
        ProjectFiscalNotExists: Se não existir projetos associados ao fiscal
        InternalServerError: Para outros erros internos
    """
    try:
        # Modificar o request para incluir o fiscal_id, page e page_size no body
        request.state.body = {
            'fiscal_id': fiscal.get('fiscal_id'),
            'page': page,
            'page_size': page_size
        }
        
        # Usar request_adapter para processar a requisição
        http_response = await request_adapter(
            request=request,
            controller=get_projects_by_fiscal_with_pagination_composer()
        )
        
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


@routes.get('/me', 
            response_model=FiscalTestResponse, 
            responses=generate_error_responses())
async def test_fiscal_mobile(
    request: Request,
    fiscal: dict = Security(fiscal_required())
):
    """
    Endpoint de teste para verificar se o fiscal está autenticado.
    
    Args:
        request: Objeto da requisição HTTP
        fiscal: Dados do fiscal autenticado (injetado pelo middleware)
        
    Returns:
        TestFiscalResponse: Dados do fiscal autenticado e timestamp
        
    Raises:
        HTTPException: Se o fiscal não estiver autenticado ou não tiver permissão
    """
    try:
        # Obtém os dados do fiscal do request.state
        fiscal_data = request.state.fiscal
        
        response_data = {
            "message": "Fiscal autenticado com sucesso!",
            "fiscal_email": fiscal_data.get("email", ""),
            "fiscal_role": fiscal_data.get("role", ""),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        log_http(
            level='INFO',
            logger_name=PREFIX,
            http_response=HttpResponse(status_code=200, body=response_data),
            request=request
        )
        
        return response_data
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            http_response=error_result,
            request=request
        )
        return response_adapter(error_result)