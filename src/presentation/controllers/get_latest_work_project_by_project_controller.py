from src.domain.use_cases.i_get_latest_work_project_by_project import IGetLatestWorkProjectByProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class GetLatestWorkProjectByProjectController(ControllerInterface):

    def __init__(self, get_latest_work_project_by_project_case: IGetLatestWorkProjectByProject) -> None:
        self.__get_latest_work_project_by_project_case = get_latest_work_project_by_project_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params['project_id']
            
            work_project = self.__get_latest_work_project_by_project_case.get_latest_by_project(project_id=project_id)
            
            if not work_project:
                return HttpResponse(
                    status_code=404,
                    body={
                        'message': 'No work projects found for this project',
                        'content': None
                    }
                )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Latest Work Project Found',
                    'content': {
                        'id': work_project.id,
                        'project_id': work_project.project_id,
                        'fiscal_id': work_project.fiscal_id,
                        'title': work_project.title,
                        'description': work_project.description,
                        'photo_name': work_project.photo_name,
                        'additional_documents': work_project.additional_documents,
                        'created_at': work_project.created_at.strftime('%Y-%m-%d %H:%M:%S') if work_project.created_at else None,
                        'updated_at': work_project.updated_at.strftime('%Y-%m-%d %H:%M:%S') if work_project.updated_at else None,
                        'fiscal': {
                            'id': work_project.fiscal.fiscal_id,
                            'name': work_project.fiscal.name,
                            'created_at': work_project.fiscal.created_at.strftime('%Y-%m-%d %H:%M:%S') if work_project.fiscal.created_at else None
                        } if work_project.fiscal else None,
                        'project': {
                            'id': work_project.project.project_id,
                            'status_id': work_project.project.status_id,
                            'name': work_project.project.name,
                            'andamento_do_projeto': work_project.project.andamento_do_projeto,
                            'verba_disponivel': str(work_project.project.verba_disponivel),
                            'start_date': work_project.project.start_date.strftime('%Y-%m-%d') if work_project.project.start_date else None,
                            'expected_completion_date': work_project.project.expected_completion_date.strftime('%Y-%m-%d') if work_project.project.expected_completion_date else None,
                            'end_date': work_project.project.end_date.strftime('%Y-%m-%d') if work_project.project.end_date else None
                        } if work_project.project else None
                    }
                }
            )
        except Exception as e:
            raise e from e 