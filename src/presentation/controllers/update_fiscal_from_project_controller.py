from src.domain.use_cases.i_update_fiscal_from_project import IUpdateFiscalFromProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateFiscalFromProjectController(ControllerInterface):

    def __init__(self, 
                 update_fiscal_from_project_case:IUpdateFiscalFromProject,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_fiscal_from_project_case = update_fiscal_from_project_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            fiscal_id = body['fiscal_id']
            new_fiscal_id = body['new_fiscal_id']
            self.__update_fiscal_from_project_case.update(
                project_id=project_id,
                fiscal_id=fiscal_id,
                new_fiscal_id=new_fiscal_id
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Fiscal',
                description=f'Fiscal do projeto atualizado de {fiscal_id} para {new_fiscal_id}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal from project updated'
                }
            )
        except Exception as e:
            raise e from e