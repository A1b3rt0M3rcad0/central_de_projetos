#pylint:disable=all
from src.domain.use_cases.i_find_all_status import IFindAllStatus
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllStatusController(ControllerInterface):

    def __init__(self, find_all_status_case:IFindAllStatus) -> None:
        self.__find_all_status_case= find_all_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            results = self.__find_all_status_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Status Founded',
                    'content': [
                        {'id': status.status_id, 'description':status.description, 'created_at':status.created_at.strftime(r'%d/%m/%Y')}
                        for status in results
                    ]
                }
            )
        except Exception as e:
            raise e from e