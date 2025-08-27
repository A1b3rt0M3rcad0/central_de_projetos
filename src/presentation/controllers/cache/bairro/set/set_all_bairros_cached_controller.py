from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class SetAllBairrosCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            # Chave fixa para lista de todos os bairros
            key = "all_bairros"
            
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
                    'message': 'All bairros cached successfully',
                    'content': {'bairros': 'cached'}
                }
            )
        except Exception as e:
            raise e from e 