from src.domain.use_cases.i_find_fiscal_by_id import IFindFiscalById
from src.domain.use_cases.i_create_project_fiscal import ICreateProjectFiscal
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateProjectFiscalController(ControllerInterface):

    def __init__(self, 
                 create_project_fiscal_case:ICreateProjectFiscal,
                 find_fiscal_by_id_case: IFindFiscalById,
                 create_history_project_case: ICreateHistoryProject
                 ) -> None:
        self.__create_project_fiscal_case = create_project_fiscal_case
        self.__find_fiscal_by_id_case = find_fiscal_by_id_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            fiscal_id = body['fiscal_id']
            self.__create_project_fiscal_case.create(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
            fiscal = self.__find_fiscal_by_id_case.find(
                fiscal_id=fiscal_id
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Fiscal',
                description=f'Fiscal: "{fiscal.name}" associado'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal associado'
                }
            )
        except Exception as e:
            raise e from e