from src.domain.use_cases.i_get_work_projects_by_fiscal_with_pagination import IGetWorkProjectsByFiscalWithPagination
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface


class GetAllWorkProjectsByFiscalMobileController(ControllerInterface):

    def __init__(self, get_work_projects_by_fiscal_with_pagination_case: IGetWorkProjectsByFiscalWithPagination) -> None:
        self.__get_work_projects_by_fiscal_with_pagination_case = get_work_projects_by_fiscal_with_pagination_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            path_params = http_request.path_params or {}
            query_params = http_request.query_params or {}

            fiscal_id = int(body.get('fiscal_id'))
            page = int(path_params.get('page'))
            page_size = int(path_params.get('page_size'))
            search_term = query_params.get('search')  # Opcional para filtro

            # Buscar work projects com filtro aplicado no repository
            result = self.__get_work_projects_by_fiscal_with_pagination_case.get_by_fiscal_with_pagination(
                fiscal_id=fiscal_id,
                page=page,
                page_size=page_size,
                search_term=search_term
            )

            work_projects_data = []
            for work_project in result['data']:
                work_project_data = {
                    'id': work_project.id,
                    'project_id': work_project.project_id,
                    'fiscal_id': work_project.fiscal_id,
                    'title': work_project.title,
                    'description': work_project.description,
                    'photo_name': work_project.photo_name,
                    'additional_documents': work_project.additional_documents,
                    'created_at': work_project.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.created_at else work_project.created_at,
                    'updated_at': work_project.updated_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.updated_at else work_project.updated_at,
                }
                # fiscal
                if getattr(work_project, 'fiscal', None):
                    work_project_data['fiscal'] = {
                        'id': work_project.fiscal.fiscal_id,
                        'name': work_project.fiscal.name,
                        'created_at': work_project.fiscal.created_at.strftime(r'%d/%m/%Y %H:%M:%S') if work_project.fiscal.created_at else work_project.fiscal.created_at,
                    }
                else:
                    work_project_data['fiscal'] = None
                # project
                if getattr(work_project, 'project', None):
                    work_project_data['project'] = {
                        'id': work_project.project.project_id,
                        'status_id': work_project.project.status_id,
                        'name': work_project.project.name,
                        'andamento_do_projeto': work_project.project.andamento_do_projeto,
                        'verba_disponivel': float(work_project.project.verba_disponivel.value) if work_project.project.verba_disponivel else None,
                        'start_date': work_project.project.start_date.strftime(r'%d/%m/%Y') if work_project.project.start_date else work_project.project.start_date,
                        'expected_completion_date': work_project.project.expected_completion_date.strftime(r'%d/%m/%Y') if work_project.project.expected_completion_date else work_project.project.expected_completion_date,
                        'end_date': work_project.project.end_date.strftime(r'%d/%m/%Y') if work_project.project.end_date else work_project.project.end_date,
                    }
                else:
                    work_project_data['project'] = None

                work_projects_data.append(work_project_data)

            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work Projects Founded',
                    'total': result['total'],
                    'page': page,
                    'page_size': page_size,
                    'fiscal_id': fiscal_id,
                    'content': work_projects_data
                }
            )
        except Exception as e:
            raise e from e


