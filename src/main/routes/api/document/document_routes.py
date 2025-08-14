#pylint:disable=W0718
#pylint:disable=W0613
from io import BytesIO
from fastapi import APIRouter
from fastapi import Request
from fastapi import UploadFile, File, Form
from fastapi.responses import StreamingResponse
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.adapters.file_adapter import file_adapter
from src.errors.error_handle import error_handler

from src.main.composers.save_document_composer import save_document_composer
from src.main.composers.get_document_composer import get_document_composer
from src.main.composers.get_document_names_composer import get_document_names_composer
from src.main.composers.delete_document_composer import delete_document_composer
from src.main.composers.delete_all_documents_from_project_composer import delete_all_documents_from_project_composer

from src.main.routes.api.document.request_format.delete_document_format import DeleteDocumentFormat
from src.main.routes.api.document.request_format.delete_all_documents_format import DeleAllDocumentsFormat
from src.main.routes.api.document.document_response.save_document_response import SaveDocumentResponse
from src.main.routes.api.document.document_response.get_all_document_names_response import GetAllDocumentNamesResponse
from src.main.routes.api.__base_response.base_message_response import BaseMessageResponse
from src.main.routes.api.__error.error_response import generate_error_responses

## Auth
from fastapi import Security
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logs
from src.logs.log_http import log_http


PREFIX = '/document'
TAGS = ['document']
routes = APIRouter(prefix=PREFIX, tags=TAGS)

@routes.post('/save', response_model=SaveDocumentResponse, responses=generate_error_responses())
async def save_document(request:Request, project_id:str=Form(...), file:UploadFile=File(...), user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para salvar/enviar documentos para um projeto.
    Apenas usuários ADMIN podem enviar documentos.
    
    Args:
        request: Objeto da requisição HTTP
        project_id: ID do projeto (via formulário)
        file: Arquivo a ser enviado (PDF, Word, Excel, etc.)
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        SaveDocumentResponse: Dados do documento salvo e localização
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        InvalidFileTypeError: Se o tipo de arquivo não for suportado
        FileTooLargeError: Se o arquivo exceder o tamanho máximo
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await file_adapter(file, save_document_composer(), project_id=project_id)
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            request=request,
            logger_name=PREFIX
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

@routes.get('/{project_id}/{document_name}', responses=generate_error_responses())
async def get_document(project_id:int, document_name:str, request:Request, user=Security(role_required(["ADMIN", "ASSESOR", "VEREADOR"]))):
    """
    Endpoint para baixar/visualizar um documento específico de um projeto.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        project_id: ID do projeto
        document_name: Nome do documento a ser baixado
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        StreamingResponse: Documento em formato binário com Content-Type apropriado
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        DocumentNotFoundError: Se o documento não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        request.path_params['document_name'] = document_name
        http_response = await request_adapter(request, get_document_composer())
        log_http(
            level='INFO',
            http_response=http_response,
            request=request,
            logger_name=PREFIX,
            message=f'Download Document from Project: (Project: {project_id}, Document_Name: {document_name})'
        )
        return StreamingResponse(
            BytesIO(http_response.body),
            media_type=http_response.headers.get('Content-Type', 'application/octet-stream'),
            headers={
                "Content-Disposition": http_response.headers.get(
                    'Content-Disposition', 
                    f'attachment; filename="{document_name}"'
                )
            }
        )
    except Exception as e:
        error_result = error_handler(e)
        log_http(
            level='ERROR',
            logger_name=PREFIX,
            request=request,
            http_response=error_result
        )
        return response_adapter(error_result)

@routes.get('/projects/{project_id}/documents', response_model=GetAllDocumentNamesResponse, responses=generate_error_responses())
async def get_all_document_names(project_id:int, request:Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Endpoint para listar todos os nomes de documentos de um projeto.
    Retorna apenas os nomes dos arquivos, não o conteúdo.
    Apenas usuários com permissões de ADMIN, VEREADOR ou ASSESSOR podem acessar.
    
    Args:
        project_id: ID do projeto
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        GetAllDocumentNamesResponse: Lista com nomes de todos os documentos do projeto
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        UnauthorizedError: Se o usuário não tiver permissão
        InternalServerError: Para outros erros internos
    """
    try:
        request.path_params['project_id'] = project_id
        http_response = await request_adapter(request, get_document_names_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            request=request,
            logger_name=PREFIX
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
async def delete_document(body:DeleteDocumentFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar um documento específico de um projeto.
    Apenas usuários ADMIN podem deletar documentos.
    
    Args:
        body: Dados do documento a ser deletado (project_id e document_name)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        DocumentNotFoundError: Se o documento não for encontrado
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_document_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            request=request,
            logger_name=PREFIX
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

@routes.delete('/all', response_model=BaseMessageResponse, responses=generate_error_responses())
async def delete_all_documents_from_project(body:DeleAllDocumentsFormat, request:Request, user=Security(role_required(["ADMIN"]))):
    """
    Endpoint para deletar todos os documentos de um projeto.
    Remove todos os arquivos associados ao projeto especificado.
    Apenas usuários ADMIN podem executar esta operação.
    
    Args:
        body: Dados do projeto (project_id)
        request: Objeto da requisição HTTP
        user: Dados do usuário autenticado (injetado pelo middleware)
        
    Returns:
        BaseMessageResponse: Mensagem de sucesso na deleção
        
    Raises:
        ProjectNotFoundError: Se o projeto não for encontrado
        UnauthorizedError: Se o usuário não for ADMIN
        InternalServerError: Para outros erros internos
    """
    try:
        http_response = await request_adapter(request, delete_all_documents_from_project_composer())
        http_response = await insert_access_token(http_response, request.state.new_access_token)
        log_http(
            level='INFO',
            http_response=http_response,
            request=request,
            logger_name=PREFIX
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