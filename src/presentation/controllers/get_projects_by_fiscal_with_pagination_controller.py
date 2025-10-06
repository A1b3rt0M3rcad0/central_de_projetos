from src.domain.use_cases.i_get_projects_by_fiscal_with_pagination import IGetProjectsByFiscalWithPagination
from src.domain.use_cases.i_find_project import IFindProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectsByFiscalWithPaginationController(ControllerInterface):

    def __init__(self, get_projects_by_fiscal_with_pagination: IGetProjectsByFiscalWithPagination, find_project_case: IFindProject) -> None:
        self.__get_projects_by_fiscal_with_pagination = get_projects_by_fiscal_with_pagination
        self.__find_project_case = find_project_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            fiscal_id = body['fiscal_id']
            page = body['page']
            page_size = body['page_size']
            
            result = self.__get_projects_by_fiscal_with_pagination.get(
                fiscal_id=fiscal_id, 
                page=int(page), 
                page_size=int(page_size)
            )
            
            # Buscar detalhes completos dos projetos
            projects_with_details = []
            for project_fiscal in result['projects']:
                project = self.__find_project_case.find(project_id=project_fiscal.project_id)
                # Tratar verba_disponivel que pode ser MonetaryValue ou float
                verba_value = None
                if project.verba_disponivel:
                    if hasattr(project.verba_disponivel, 'value'):
                        verba_value = float(project.verba_disponivel.value)
                    else:
                        verba_value = float(project.verba_disponivel)
                
                projects_with_details.append({
                    'id': project.project_id,
                    'status_id': project.status_id,
                    'verba_disponivel': verba_value,
                    'andamento_do_projeto': project.andamento_do_projeto,
                    'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else None,
                    'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else None,
                    'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else None,
                    'name': project.name
                })
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'page': result['page'],
                    'page_size': result['page_size'],
                    'total_items': result['total_items'],
                    'total_pages': result['total_pages'],
                    'content': projects_with_details
                }
            )
        except Exception as e:
            raise e from e 