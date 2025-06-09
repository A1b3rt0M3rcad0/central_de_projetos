from src.domain.use_cases.i_find_all_projects_with_basic_details import IFindAllProjectsWithBasicDetails
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindAllProjectsWithBasicDetailsController(ControllerInterface):

    def __init__(self, find_all_projects_with_basic_details_case:IFindAllProjectsWithBasicDetails) -> None:
        self.__find_all_projects_with_basic_details_case = find_all_projects_with_basic_details_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__find_all_projects_with_basic_details_case.find()
            response = [
                {
                    "id": project.project_id,
                    "name": project.name,
                    "bairro": project.bairro.name if project.bairro else None,
                    "empresa": project.empresas.name if project.empresas else None,
                    "fiscal": project.fiscal.name if project.fiscal else None,
                    "status": project.status.description if project.status else None,
                    "andamento_do_projeto": project.andamento_do_projeto,
                    "user": None ## Adicionar nome do vereador
                
                } for project in result
            ]
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Projects founded",
                    "content": response
                }
            )
        except Exception as e:
            raise e from e