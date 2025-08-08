from src.domain.use_cases.i_delete_work_project import IDeleteWorkProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteWorkProjectController(ControllerInterface):

    def __init__(self, delete_work_project_case:IDeleteWorkProject) -> None:
        self.__delete_work_project_case = delete_work_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            work_project_id = int(path_params['work_project_id'])
            
            self.__delete_work_project_case.delete(work_project_id=work_project_id)
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work Project deleted successfully',
                    'work_project_id': work_project_id
                }
            )
        except Exception as e:
            raise e from e 