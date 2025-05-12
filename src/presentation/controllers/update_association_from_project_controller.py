from src.domain.use_cases.i_update_association_from_project import IUpdateAssociationFromProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateAssociationFromProjectController(ControllerInterface):

    def __init__(self, 
                 update_association_from_project_case:IUpdateAssociationFromProject,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_association_from_project_case = update_association_from_project_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            new_cpf = CPF(body['new_cpf'])
            project_id = body['project_id']
            self.__update_association_from_project_case.update(
                cpf=cpf,
                project_id=project_id,
                new_cpf=new_cpf
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='cpf',
                description=f'usuario associado trocado de {cpf.value} para {new_cpf.value}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': f'User {cpf.value} updated from project {project_id} for {new_cpf}'
                }
            )
        except Exception as e:
            raise e from e