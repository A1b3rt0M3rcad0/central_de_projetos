from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class SetProjectsWithPaginationCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            path_params = http_request.path_params
            page_size = path_params.get('page_size')
            page = path_params.get('page')
            
            if not page_size or not page:
                # Se não encontrar os parâmetros nos path_params, tenta pegar do body
                body = http_request.body
                if isinstance(body, dict):
                    page_size = page_size or body.get('page_size')
                    page = page or body.get('page')
                
                if not page_size or not page:
                    raise ValueError("page_size and page not found in request")
            
            # Chave específica para paginação
            key = f"projects_pagination_{page_size}_{page}"
            
            # Serializa os dados para armazenar no cache
            # O body pode ser um número, string, dict, list, etc.
            if isinstance(body, (dict, list)):
                value_to_cache = json.dumps(body)
            elif isinstance(body, (int, float)):
                value_to_cache = str(body)
            elif isinstance(body, str):
                value_to_cache = body
            else:
                value_to_cache = str(body)
            
            await self.set_cached_value.set(key=key, value=value_to_cache)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects with pagination cached successfully',
                    'content': {'projects': 'cached'}
                }
            )
        except Exception as e:
            raise e from e 