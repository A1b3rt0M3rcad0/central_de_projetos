from src.presentation.interface.async_controller_interface import AsyncControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_cached_value import IGetCachedValue

class FindBairroByNameCachedController(AsyncControllerInterface):
    def __init__(self, get_cached_value: IGetCachedValue):
        self.get_cached_value = get_cached_value

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['bairro_name']
            result = await self.get_cached_value.get(key=name)
            return HttpResponse(
                status_code=200,
                body={
                    'messsage': 'Bairro Founded',
                    'content': {'id':result.bairro, 'name':result.name, 'created_at':result.created_at.strftime(r'%d/%m/%Y')}
                }
            )
        except Exception as e:
            raise e from e