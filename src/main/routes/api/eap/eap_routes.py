#pylint:disable=W0718
#pylint:disable=W0613
#pylint:disable=W9016
from fastapi import APIRouter, Request, Security
from src.main.adapters.request_adapter import request_adapter
from src.main.adapters.response_adapter import response_adapter
from src.errors.error_handle import error_handler

from src.main.composers.create_eap_composer import create_eap_composer
from src.main.composers.find_eap_composer import find_eap_composer
from src.main.composers.create_eap_item_composer import create_eap_item_composer
from src.main.composers.update_eap_composer import update_eap_composer
from src.main.composers.update_eap_item_composer import update_eap_item_composer
from src.main.composers.delete_eap_composer import delete_eap_composer
from src.main.composers.delete_eap_item_composer import delete_eap_item_composer

# Auth
from src.main.routes.middleware.authorization import role_required
from src.main.routes.middleware.insert_access_token import insert_access_token

# Logger
from src.logs.log_http import log_http

PREFIX = '/eap'
TAGS = ['EAP']
router = APIRouter(prefix=PREFIX, tags=TAGS)


@router.post("/")
async def create_eap(request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Cria uma nova EAP
    
    Apenas usuários ADMIN podem criar EAPs.
    
    - **name**: Nome da EAP
    - **description**: Descrição da EAP
    - **project_id**: ID do projeto (opcional para templates)
    - **created_by**: CPF do usuário criador
    - **template_source_id**: ID da EAP template (opcional)
    """
    try:
        http_response = await request_adapter(request, create_eap_composer())
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


@router.get("/")
async def find_eap(request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Busca EAPs
    
    Usuários ADMIN, VEREADOR e ASSESSOR podem visualizar EAPs.
    
    - **eap_id**: ID específico da EAP
    - **project_id**: ID do projeto para buscar sua EAP
    - **templates**: Se True, busca apenas templates
    - **name**: Nome ou parte do nome para busca
    - **limit**: Limite de resultados (padrão: 50)
    - **offset**: Offset para paginação (padrão: 0)
    """
    try:
        http_response = await request_adapter(request, find_eap_composer())
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


@router.put("/{eap_id}")
async def update_eap(request: Request, eap_id: int, user=Security(role_required(["ADMIN"]))):
    """
    Atualiza uma EAP existente
    
    Apenas usuários ADMIN podem atualizar EAPs.
    
    - **eap_id**: ID da EAP a ser atualizada
    - **name**: Novo nome da EAP (opcional)
    - **description**: Nova descrição da EAP (opcional)
    """
    try:
        # Adiciona o eap_id aos path params
        request.path_params['eap_id'] = eap_id
        
        http_response = await request_adapter(request, update_eap_composer())
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


@router.post("/items")
async def create_eap_item(request: Request, user=Security(role_required(["ADMIN"]))):
    """
    Cria um novo item da EAP
    
    Apenas usuários ADMIN podem criar itens da EAP.
    
    - **eap_id**: ID da EAP
    - **code**: Código hierárquico (ex: "1.1.1")
    - **name**: Nome do item
    - **description**: Descrição do item
    - **type**: Tipo (fase, entrega, atividade, tarefa)
    - **parent_id**: ID do item pai (opcional para itens raiz)
    - **responsible**: Responsável pelo item
    - **start_date**: Data de início (ISO format)
    - **end_date**: Data de fim (ISO format)
    - **budget**: Orçamento do item
    - **status**: Status inicial (opcional, padrão: nao_iniciado)
    - **progress**: Progresso inicial (opcional, padrão: 0)
    """
    try:
        http_response = await request_adapter(request, create_eap_item_composer())
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


@router.put("/items/{item_id}")
async def update_eap_item(request: Request, item_id: int, user=Security(role_required(["ADMIN"]))):
    """
    Atualiza um item da EAP existente
    
    Apenas usuários ADMIN podem atualizar itens da EAP.
    
    - **item_id**: ID do item a ser atualizado
    - Campos opcionais: name, description, responsible, start_date, end_date, budget, status, progress
    """
    try:
        # Adiciona o item_id aos path params
        request.path_params['item_id'] = item_id
        
        http_response = await request_adapter(request, update_eap_item_composer())
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


@router.delete("/{eap_id}")
async def delete_eap(request: Request, eap_id: int, user=Security(role_required(["ADMIN"]))):
    """
    Exclui uma EAP existente
    
    Apenas usuários ADMIN podem excluir EAPs.
    
    - **eap_id**: ID da EAP a ser excluída
    """
    try:
        # Adiciona o eap_id aos path params
        request.path_params['eap_id'] = eap_id
        
        http_response = await request_adapter(request, delete_eap_composer())
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


@router.delete("/items/{item_id}")
async def delete_eap_item(request: Request, item_id: int, user=Security(role_required(["ADMIN"]))):
    """
    Exclui um item da EAP existente
    
    Apenas usuários ADMIN podem excluir itens da EAP.
    
    - **item_id**: ID do item a ser excluído
    """
    try:
        # Adiciona o item_id aos path params
        request.path_params['item_id'] = item_id
        
        http_response = await request_adapter(request, delete_eap_item_composer())
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


@router.get("/project/{project_id}")
async def get_project_eap(request: Request, project_id: int, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Busca a EAP de um projeto específico
    
    Usuários ADMIN, VEREADOR e ASSESSOR podem visualizar EAPs de projetos.
    
    - **project_id**: ID do projeto
    """
    try:
        # Adiciona o project_id aos path params
        request.path_params['project_id'] = project_id
        
        http_response = await request_adapter(request, find_eap_composer())
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


@router.get("/templates")
async def get_eap_templates(request: Request, user=Security(role_required(["ADMIN", "VEREADOR", "ASSESSOR"]))):
    """
    Busca todas as EAPs que são templates
    
    Usuários ADMIN, VEREADOR e ASSESSOR podem visualizar templates de EAP.
    """
    try:
        # Adiciona o parâmetro templates aos query params
        if not hasattr(request, 'query_params') or request.query_params is None:
            request.query_params = {}
        request.query_params["templates"] = "true"
        
        http_response = await request_adapter(request, find_eap_composer())
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
