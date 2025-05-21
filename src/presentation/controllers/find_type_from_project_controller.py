from src.domain.use_cases.i_find_type_from_project import IFindTypeFromProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindTypeFromProjectController(ControllerInterface):

    def __init__(self, find_type_from_project_case:IFindTypeFromProject) -> None:
        self.__find_type_from_project_case = find_type_from_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params['project_id']
            associations = self.__find_type_from_project_case.find(
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Type Founded',
                    'content': [
                        {
                            'project_id': association.project_id,
                            'types_id': association.types_id,
                            'created_at': association.created_at
                        }
                        for association in associations
                    ]
                }
            )
        except Exception as e:
            raise e from e