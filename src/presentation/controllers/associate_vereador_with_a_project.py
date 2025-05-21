from src.domain.use_cases.i_associate_vereador_with_a_project import IAssociateVereadorWithAProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.cpf import CPF

class AssociateVereadorWithAProjectController(ControllerInterface):

    def __init__(self, associate_vereador_with_a_project_case:IAssociateVereadorWithAProject) -> None:
        self.__associate_vereador_with_a_project_case =associate_vereador_with_a_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = body['cpf']
            project_id = body['project_id']
            self.__associate_vereador_with_a_project_case.associate(
                cpf_user=CPF(cpf),
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Association Created'
                }
            )
        except Exception as e:
            raise e from e