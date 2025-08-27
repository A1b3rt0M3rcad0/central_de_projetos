from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_cached_value import IGetCachedValue
import json

class FindBairroByNameCachedController(AsyncControllerInterface):
    def __init__(self, get_cached_value: IGetCachedValue):
        self.get_cached_value = get_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['bairro_name']
            result = await self.get_cached_value.get(key=name)
            
            # Se não encontrou no cache, retorna None no content
            if result is None:
                return HttpResponse(
                    status_code=200,
                    body={'content': None}
                )
            
            # Se encontrou, retorna os dados do cache
            # O resultado do cache pode ser uma string JSON ou um objeto
            if isinstance(result, str):
                try:
                    # Tenta fazer parse do JSON
                    cached_data = json.loads(result)
                    return HttpResponse(
                        status_code=200,
                        body={
                            'messsage': 'Bairro Founded',
                            'content': cached_data
                        }
                    )
                except json.JSONDecodeError:
                    # Se não for JSON válido, retorna como string
                    return HttpResponse(
                        status_code=200,
                        body={
                            'messsage': 'Bairro Founded',
                            'content': result
                        }
                    )
            else:
                # Se já for um objeto/dicionário
                return HttpResponse(
                    status_code=200,
                    body={
                        'messsage': 'Bairro Founded',
                        'content': result
                    }
                )
        except Exception as e:
            raise e from e