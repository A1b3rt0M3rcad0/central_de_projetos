from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_get_cached_value import IGetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import json

class GetAllProjectsCachedController(AsyncControllerInterface):
    def __init__(self, get_cached_value: IGetCachedValue):
        self.get_cached_value = get_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Chave fixa para lista de todos os projetos
            key = "all_projects"
            
            cached_value = await self.get_cached_value.get(key=key)
            
            if cached_value is not None:
                # Tenta deserializar o valor do cache
                try:
                    # Primeiro tenta como JSON
                    projects_data = json.loads(cached_value)
                except (json.JSONDecodeError, TypeError):
                    # Se não for JSON, tenta como número
                    try:
                        projects_data = int(cached_value)
                    except (ValueError, TypeError):
                        try:
                            projects_data = float(cached_value)
                        except (ValueError, TypeError):
                            # Se não conseguir converter, usa como string
                            projects_data = cached_value
                
                return HttpResponse(
                    status_code=200,
                    body={
                        'message': 'Projects retrieved from cache',
                        'content': projects_data
                    }
                )
            
            # Cache miss - retorna None para buscar no banco
            return HttpResponse(
                status_code=200,
                body={'content': None}
            )
            
        except Exception as e:
            raise e from e 