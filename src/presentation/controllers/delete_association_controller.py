from src.domain.use_cases.i_delete_association import IDeleteAssociation
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteAssociationController(ControllerInterface):

    def __init__(self, 
                 delete_association_case:IDeleteAssociation,
                 create_history_project_case:ICreateHistoryProject):
        self.__delete_association_case = delete_association_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            project_id = body['project_id']
            
            # Deletar a associação usuário-projeto
            self.__delete_association_case.delete(
                cpf = cpf,
                project_id=project_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Associação',
                description=f'Usuário {cpf.value} removido do projeto'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Association Deleted'
                }
            )
        except Exception as e:
            raise e from e