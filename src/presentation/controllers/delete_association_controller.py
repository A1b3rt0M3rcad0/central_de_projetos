from src.domain.use_cases.i_delete_association import IDeleteAssociation
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteAssociationController(ControllerInterface):

    def __init__(self, delete_association_case:IDeleteAssociation):
        self.__delete_association_case = delete_association_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            project_id = body['project_id']
            self.__delete_association_case.delete(
                cpf = cpf,
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Association Deleted'
                }
            )
        except Exception as e:
            raise e from e