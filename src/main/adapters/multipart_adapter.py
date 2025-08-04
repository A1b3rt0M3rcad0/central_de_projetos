from fastapi import Request as FastAPIRequest, UploadFile
from typing import Callable, Dict, Any, Optional, List
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


async def multipart_adapter(
    request: FastAPIRequest,
    controller: Callable[[HttpRequest], HttpResponse],
    form_data: Dict[str, Any],
    files: Optional[List[UploadFile]] = None,
    single_file: Optional[UploadFile] = None
) -> HttpResponse:
    """
    Adapter para lidar com multipart/form-data que combina dados do formulário com arquivos.
    
    Args:
        request: Request do FastAPI
        controller: Controller a ser executado
        form_data: Dados do formulário (project_id, fiscal_id, title, description, etc.)
        files: Lista de arquivos (opcional)
        single_file: Arquivo único (opcional)
    """
    
    # Prepara os dados dos arquivos
    additional_documents = []
    
    # Processa arquivo único se fornecido
    if single_file:
        file_content = await single_file.read()
        additional_documents.append({
            "name": single_file.filename,
            "content": file_content,
            "content_type": single_file.content_type
        })
    
    # Processa lista de arquivos se fornecida
    if files:
        for file in files:
            file_content = await file.read()
            additional_documents.append({
                "name": file.filename,
                "content": file_content,
                "content_type": file.content_type
            })
    
    # Combina os dados do formulário com os documentos
    body = {
        **form_data,
        "additional_documents": additional_documents
    }

    http_request = HttpRequest(
        body=body,
        headers=dict(request.headers),
        query_params=dict(request.query_params),
        path_params=request.path_params,
        url=str(request.url)
    )

    http_response = controller(http_request)
    return http_response 