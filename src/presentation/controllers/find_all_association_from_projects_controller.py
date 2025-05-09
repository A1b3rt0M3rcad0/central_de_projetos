#pylint:disable=all;
from src.domain.use_cases.i_find_all_association_from_projects import IFindAllAssociationfromProjects
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllAssociationFromProjectsController(ControllerInterface):

    def __init__(self, find_all_association_from_projects_case:IFindAllAssociationfromProjects) -> None:
        self.__find_all_association_from_projects_case = find_all_association_from_projects_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            results = self.__find_all_association_from_projects_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Association From Projects Founded',
                    'content': [
                        [association.cpf, association.project_id, association.data_atriuicao]
                        for association in results
                    ]
                }
            )
        except Exception as e:
            raise e from e