from src.domain.use_cases.i_delete_work_project_by_fiscal import IDeleteWorkProjectByFiscal
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteWorkProjectMobileController(ControllerInterface):

    def __init__(self, 
                 delete_work_project_by_fiscal_case: IDeleteWorkProjectByFiscal,
                 create_history_project_case: ICreateHistoryProject) -> None:
        self.__delete_work_project_by_fiscal_case = delete_work_project_by_fiscal_case
        self.__create_history_project_case = create_history_project_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            # Obter dados do path_params e body
            path_params = http_request.path_params or {}
            body = http_request.body or {}
            
            # Dados do work project
            work_project_id = int(path_params.get('work_project_id'))
            fiscal_id = body.get('fiscal_id')
            
            if not fiscal_id:
                return HttpResponse(
                    status_code=400,
                    body={'error': 'fiscal_id is required'}
                )
            
            # Deletar o work project e seus documentos
            self.__delete_work_project_by_fiscal_case.delete(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=body.get('project_id', 0),  # Pode ser obtido do work project se necessário
                data_name='Work Project Mobile',
                description=f'Work project {work_project_id} deletado via mobile pelo fiscal {fiscal_id}'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work project deleted successfully via mobile',
                    'work_project_id': work_project_id,
                    'fiscal_id': fiscal_id
                }
            )

        except Exception as e:
            raise e from e 