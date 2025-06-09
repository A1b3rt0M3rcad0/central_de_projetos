from src.domain.use_cases.i_find_all_projects_with_basic_details import IFindAllProjectsWithBasicDetails
from src.domain.use_cases.i_find_user_by_project_id import IFindUserByProjectId
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindAllProjectsWithBasicDetailsController(ControllerInterface):

    def __init__(self, find_all_projects_with_basic_details_case:IFindAllProjectsWithBasicDetails, find_user_by_project_id_case:IFindUserByProjectId) -> None:
        self.__find_all_projects_with_basic_details_case = find_all_projects_with_basic_details_case
        self.__find_user_by_project_id_case = find_user_by_project_id_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__find_all_projects_with_basic_details_case.find()
            response = []
            for project in result:
                user = self.__find_user_by_project_id_case.find(project.project_id)
                project = {
                    "id": project.project_id,
                    "name": project.name,
                    "bairro": project.bairro.name if project.bairro else None,
                    "empresa": project.empresas.name if project.empresas else None,
                    "fiscal": project.fiscal.name if project.fiscal else None,
                    "status": project.status.description if project.status else None,
                    "andamento_do_projeto": project.andamento_do_projeto,
                    "user": user.name if user else user
                }
                response.append(project)
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Projects founded",
                    "content": response
                }
            )
        except Exception as e:
            raise e from e