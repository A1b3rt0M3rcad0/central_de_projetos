from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class SetProjectDetailCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            path_params = http_request.path_params
            project_id = path_params.get('project_id')
            if not project_id:
                # Se não encontrar project_id nos path_params, tenta pegar do body
                body = http_request.body
                if isinstance(body, dict) and 'project_id' in body:
                    project_id = body['project_id']
                else:
                    raise ValueError("project_id not found in request")
            
            # Chave específica para detalhes do projeto
            key = f"project_detail_{project_id}"
            
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
                    'message': 'Project detail cached successfully',
                    'content': {'project_detail': 'cached'}
                }
            )
        except Exception as e:
            raise e from e 