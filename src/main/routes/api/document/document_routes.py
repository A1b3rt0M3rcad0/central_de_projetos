#pylint:disable=W0718
#pylint:disable=W0613
#pylint:disable=all
from fastapi import APIRouter
from fastapi import Request
from fastapi import UploadFile, File, Form
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.main.adapters.file_adapter import file_adapter
from src.errors.error_handle import error_handler

from src.main.composers.save_document_composer import save_document_composer

routes = APIRouter(prefix='/document', tags=['document'])

@routes.post('/save')
async def save_document(project_id:str=Form(...), file:UploadFile=File(...)):
    try:
        http_response = await file_adapter(file, save_document_composer(), project_id=project_id)
        return response_adapter(http_response)
    except Exception as e:
        return response_adapter(error_handler(e))