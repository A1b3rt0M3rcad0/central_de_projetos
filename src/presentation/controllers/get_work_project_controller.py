from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class GetWorkProjectController(ControllerInterface):

    def __init__(self, get_work_project_case:IGetWorkProject) -> None:
        self.__get_work_project_case = get_work_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            work_project_id = path_params['work_project_id']
            work_project = self.__get_work_project_case.get(work_project_id=work_project_id)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work Project Founded',
                    'content': {
                        'id': work_project.id,
                        'project_id': work_project.project_id,
                        'fiscal_id': work_project.fiscal_id,
                        'title': work_project.title,
                        'description': work_project.description,
                        'photo_name': work_project.photo_name,
                        'additional_documents': work_project.additional_documents,
                        'created_at': work_project.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.created_at else work_project.created_at,
                        'updated_at': work_project.updated_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.updated_at else work_project.updated_at,
                        'fiscal': {
                            'id': work_project.fiscal.fiscal_id,
                            'name': work_project.fiscal.name,
                            'created_at': work_project.fiscal.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.fiscal.created_at else work_project.fiscal.created_at
                        } if work_project.fiscal else None,
                        'project': {
                            'id': work_project.project.project_id,
                            'status_id': work_project.project.status_id,
                            'name': work_project.project.name,
                            'andamento_do_projeto': work_project.project.andamento_do_projeto,
                            'verba_disponivel': float(work_project.project.verba_disponivel.value) if work_project.project.verba_disponivel else None,
                            'start_date': work_project.project.start_date.strftime(r'%d/%m/%Y') if work_project.project.start_date else work_project.project.start_date,
                            'expected_completion_date': work_project.project.expected_completion_date.strftime(r'%d/%m/%Y') if work_project.project.expected_completion_date else work_project.project.expected_completion_date,
                            'end_date': work_project.project.end_date.strftime(r'%d/%m/%Y') if work_project.project.end_date else work_project.project.end_date
                        } if work_project.project else None
                    }
                }
            )
        except Exception as e:
            raise e from e 