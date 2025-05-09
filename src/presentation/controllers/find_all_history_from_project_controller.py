from src.domain.use_cases.i_find_all_history_from_project import IFindAllHistoryFromProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllHistoryFromProjectController(ControllerInterface):

    def __init__(self, find_all_history_from_project:IFindAllHistoryFromProject):
        self.__find_all_history_from_project = find_all_history_from_project
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            results = self.__find_all_history_from_project.find(project_id=project_id)
            return HttpResponse(
                status_code=200,
                body={
                    'message':'History from project founded',
                    'content': {[
                        [history.history_project_id, 
                         history.project_id, 
                         history.data_name, 
                         history.description,
                         history.updated_at]
                        for history in results
                    ]}
                }
            )
        except Exception as e:
            raise e from e