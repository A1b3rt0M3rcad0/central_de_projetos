from src.domain.use_cases.i_update_project_verba import IUpdateProjectVerba
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.value_objects.monetary_value import MonetaryValue
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateProjectVerbaController(ControllerInterface):

    def __init__(self, 
                 update_project_verba_case:IUpdateProjectVerba,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_project_verba_case = update_project_verba_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            verba_disponivel = body['verba_disponivel']
            self.__update_project_verba_case.update(
                project_id=project_id,
                verba_disponivel=MonetaryValue(verba_disponivel)
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Verba Disponivel',
                description=f'Verba Disponivel atualizada para {verba_disponivel}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'verba_disponivel updated'
                }
            )
        except Exception as e:
            raise e from e