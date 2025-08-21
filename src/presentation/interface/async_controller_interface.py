from abc import ABC, abstractmethod
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class AsyncControllerInterface(ABC):

    @abstractmethod
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        """
        Handle an incoming HTTP request and return an HTTP response.
        """