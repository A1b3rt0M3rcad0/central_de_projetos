#pylint:disable=W0718
#pylint:disable=W0613
from fastapi import APIRouter, UploadFile, File, Form
from fastapi import Request
from typing import List
from src.main.adapters.multipart_adapter import multipart_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_work_project_with_fiscal_document_composer import create_work_project_with_fiscal_document_composer

from src.main.routes.api.__error.error_response import generate_error_responses
from src.main.routes.api.work_project.work_project_response.create_work_project_with_fiscal_document_response import CreateWorkProjectWithFiscalDocumentResponse

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
    user = Security(role_required(["ADMIN"]))
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