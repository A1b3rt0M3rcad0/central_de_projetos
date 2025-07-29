from src.domain.use_cases.i_get_projects_with_pagination import IGetProjectsWithPagination
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectsWithPaginationController(ControllerInterface):

    def __init__(self, get_projects_with_pagination:IGetProjectsWithPagination) -> None:
        self.__get_projects_with_pagination = get_projects_with_pagination

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            result = self.__get_projects_with_pagination.get(page=int(page), page_size=int(page_size))
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project page founded',
                    'content': {
                        'page': result.get('page'),
                        'page_size': result.get('page_size'),
                        'total_items': result.get('total_items'),
                        'total_pages': result.get('total_pages'),
                        'projects': [
                            {
                                'id': project.project_id,
                                'verba_disponivel': float(project.verba_disponivel.value),
                                'andamento_do_projeto': project.andamento_do_projeto,
                                'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else None,
                                'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else None,
                                'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else None,
                                'status_id': project.status_id,
                                'name': project.name,
                                'bairro': {
                                    'id': project.bairro.bairro,
                                    'name': project.bairro.name,
                                    'created_at': project.bairro.created_at.strftime(r'%d/%m/%Y') if project.bairro and project.bairro.created_at else None
                                } if project.bairro else None,
                                'empresa': {
                                    'id': project.empresa.empresa_id,
                                    'name': project.empresa.name,
                                    'created_at': project.empresa.created_at.strftime(r'%d/%m/%Y') if project.empresa and project.empresa.created_at else None
                                } if hasattr(project, 'empresa') and project.empresa else None,
                                'fiscal': {
                                    'id': project.fiscal.fiscal_id,
                                    'name': project.fiscal.name,
                                    'created_at': project.fiscal.created_at.strftime(r'%d/%m/%Y') if project.fiscal and project.fiscal.created_at else None
                                } if hasattr(project, 'fiscal') and project.fiscal else None,
                                'types': {
                                    'id': project.types.types_id,
                                    'name': project.types.name,
                                    'created_at': project.types.created_at.strftime(r'%d/%m/%Y') if project.types and project.types.created_at else None
                                } if hasattr(project, 'types') and project.types else None,
                                'status': {
                                    'id': project.status.status_id,
                                    'description': project.status.description,
                                    'created_at': project.status.created_at.strftime(r'%d/%m/%Y') if project.status and project.status.created_at else None
                                } if hasattr(project, 'status') and project.status else None
                            }
                            for project in result.get('projects')
                        ]
                    }
                }
            )
        except Exception as e:
            raise e from e