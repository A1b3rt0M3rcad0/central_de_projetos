from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.domain.use_cases.i_set_cached_value import ISetCachedValue
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class SetBairroByNameCachedController(AsyncControllerInterface):
    def __init__(self, set_cached_value: ISetCachedValue):
        self.set_cached_value = set_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            body = http_request.body
            name = path_params['name']
            await self.set_cached_value.set(key=name, value=body)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairro set successfully',
                    'content': {'name': name}
                }
            )
        except Exception as e:
            raise e from e