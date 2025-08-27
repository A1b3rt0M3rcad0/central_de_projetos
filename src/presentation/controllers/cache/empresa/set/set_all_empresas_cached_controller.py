from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class SetAllEmpresasCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            
            # Serializa os dados para armazenar no cache
            if isinstance(body, (dict, list)):
                value_to_cache = json.dumps(body)
            else:
                value_to_cache = str(body)
            
            # Chave fixa para todas as empresas
            key = 'all_empresas'
            await self.set_cached_value.set(key=key, value=value_to_cache)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'All empresas set successfully',
                    'content': {'key': key}
                }
            )
        except Exception as e:
            raise e from e 