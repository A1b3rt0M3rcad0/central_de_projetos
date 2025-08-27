#pylint:disable=W0718,W0613
from fastapi import Request as FastAPIRequest
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable, Optional, Dict
import inspect

async def generic_cache_aside_adapter(
    framework_request: FastAPIRequest,
    cache_get_controller: Callable[[HttpRequest], HttpResponse],
    db_controller: Callable[[HttpRequest], HttpResponse],
    cache_set_controller: Callable[[HttpRequest], HttpResponse],
    cache_key_mapping: Dict[str, str],
    cache_ttl: Optional[int] = None
) -> HttpResponse:
    """
    Adapter genérico que implementa o padrão cache-aside.
    
    Fluxo:
    1. Tenta buscar no cache primeiro
    2. Se não encontrar, busca no banco de dados
    3. Se encontrar no banco, armazena no cache
    4. Retorna o resultado para o cliente
    
    Args:
        framework_request: Requisição do FastAPI
        cache_get_controller: Controller para buscar no cache
        db_controller: Controller para buscar no banco de dados
        cache_set_controller: Controller para armazenar no cache
        cache_key_mapping: Mapeamento de parâmetros para chaves de cache
                          Ex: {'bairro_name': 'bairro_name', 'user_id': 'user_id'}
        cache_ttl: Tempo de vida do cache em segundos (opcional)
        
    Returns:
        HttpResponse: Resposta com os dados encontrados
    """
    
    # Converte FastAPIRequest para HttpRequest
    http_request = HttpRequest(
        body={},
        headers=dict(framework_request.headers),
        query_params=dict(framework_request.query_params),
        path_params=framework_request.path_params,
        url=str(framework_request.url),
    )
    
    # Função auxiliar para executar controllers síncronos ou assíncronos
    async def execute_controller(controller, request):
        if inspect.iscoroutinefunction(controller):
            return await controller(request)
        return controller(request)
    
    try:
        # 1. Tenta buscar no cache primeiro
        cache_response = await execute_controller(cache_get_controller, http_request)
        
        # Se encontrou no cache, retorna diretamente
        if cache_response.status_code == 200 and cache_response.body.get('content') is not None:
            return cache_response
            
    except Exception:
        # Se deu erro no cache, continua para o banco
        pass
    
    try:
        # 2. Busca no banco de dados
        db_response = await execute_controller(db_controller, http_request)
        
        # Se encontrou no banco e foi bem-sucedido
        if db_response.status_code == 200 and db_response.body.get('content') is not None:
            try:
                # 3. Prepara os parâmetros para o cache
                cache_path_params = {}
                for param_key, cache_key in cache_key_mapping.items():
                    if param_key in http_request.path_params:
                        cache_path_params[cache_key] = http_request.path_params[param_key]
                
                # 3. Armazena no cache para próximas consultas
                # IMPORTANTE: Não armazena o access_token no cache
                cache_body = db_response.body.get('content', {})
                if isinstance(cache_body, dict) and 'access_token' in cache_body:
                    # Remove o access_token antes de armazenar no cache
                    cache_body = {k: v for k, v in cache_body.items() if k != 'access_token'}
                
                cache_set_request = HttpRequest(
                    body=cache_body,
                    headers=http_request.headers,
                    query_params=http_request.query_params,
                    path_params=cache_path_params,
                    url=http_request.url,
                )
                
                await execute_controller(cache_set_controller, cache_set_request)
            except Exception:
                # Se falhar ao armazenar no cache, não falha a requisição
                # Apenas loga o erro (pode ser implementado depois)
                pass
            
            # 4. Retorna o resultado do banco
            return db_response
            
    except Exception as e:
        # Se não encontrou no banco, propaga o erro
        raise e
    
    # Se chegou aqui, não encontrou nem no cache nem no banco
    return db_response

async def simple_cache_aside_adapter(
    framework_request: FastAPIRequest,
    cache_get_controller: Callable[[HttpRequest], HttpResponse],
    db_controller: Callable[[HttpRequest], HttpResponse],
    cache_set_controller: Callable[[HttpRequest], HttpResponse],
    cache_key: str
) -> HttpResponse:
    """
    Versão simplificada do cache-aside adapter para casos com uma única chave.
    
    Args:
        framework_request: Requisição do FastAPI
        cache_get_controller: Controller para buscar no cache
        db_controller: Controller para buscar no banco de dados
        cache_set_controller: Controller para armazenar no cache
        cache_key: Chave para buscar/armazenar no cache
        
    Returns:
        HttpResponse: Resposta com os dados encontrados
    """
    return await generic_cache_aside_adapter(
        framework_request=framework_request,
        cache_get_controller=cache_get_controller,
        db_controller=db_controller,
        cache_set_controller=cache_set_controller,
        cache_key_mapping={cache_key: cache_key}
    ) 