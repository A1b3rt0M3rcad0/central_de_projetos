from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_get_cached_value import IGetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class GetCountProjectsCachedController(AsyncControllerInterface):
    def __init__(self, get_cached_value: IGetCachedValue):
        self.get_cached_value = get_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Chave fixa para contagem de projetos
            key = "count_projects"
            
            cached_value = await self.get_cached_value.get(key=key)
            
            if cached_value is not None:
                # Tenta deserializar o valor do cache
                try:
                    # Primeiro tenta como JSON
                    count_data = json.loads(cached_value)
                except (json.JSONDecodeError, TypeError):
                    # Se não for JSON, tenta como número
                    try:
                        count_data = int(cached_value)
                        # Formata o número para o formato esperado pela API
                        count_data = {"projects": count_data}
                    except (ValueError, TypeError):
                        try:
                            count_data = float(cached_value)
                            # Formata o número para o formato esperado pela API
                            count_data = {"projects": int(count_data)}
                        except (ValueError, TypeError):
                            # Se não conseguir converter, usa como string
                            count_data = cached_value
                
                # Debug: verifica se o formato está correto
                if isinstance(count_data, dict) and 'projects' in count_data:
                    return HttpResponse(
                        status_code=200,
                        body={
                            'message': 'Count retrieved from cache',
                            'content': count_data
                        }
                    )
                # Se não estiver no formato correto, retorna None para buscar no banco
                return HttpResponse(
                    status_code=200,
                    body={'content': None}
                )
            
            # Cache miss - retorna None para buscar no banco
            return HttpResponse(
                status_code=200,
                body={'content': None}
            )
            
        except Exception as e:
            raise e from e 