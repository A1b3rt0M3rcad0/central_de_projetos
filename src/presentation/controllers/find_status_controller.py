from src.domain.use_cases.i_find_status import IFindStatus
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindStatusController(ControllerInterface):

    def __init__(self, find_status_case:IFindStatus) -> None:
        self.__find_status_code = find_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            status_id = path_params['status_id']
            status = self.__find_status_code.find(status_id=status_id)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Status Founded',
                    'content': {
                        'id': status.status_id,
                        'description': status.description,
                        'created_at': status.created_at.strftime(r'%d/%m/%Y')
                    }
                }
            )
        except Exception as e:
            raise e from e