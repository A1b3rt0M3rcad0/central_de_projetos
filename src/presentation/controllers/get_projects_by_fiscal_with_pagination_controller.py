from src.domain.use_cases.i_get_projects_by_fiscal_with_pagination import IGetProjectsByFiscalWithPagination
from src.domain.use_cases.i_find_project import IFindProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectsByFiscalWithPaginationController(ControllerInterface):

    def __init__(self, get_projects_by_fiscal_with_pagination: IGetProjectsByFiscalWithPagination, find_project_case: IFindProject, work_project_repository: IWorkProjectRepository) -> None:
        self.__get_projects_by_fiscal_with_pagination = get_projects_by_fiscal_with_pagination
        self.__find_project_case = find_project_case
        self.__work_project_repository = work_project_repository

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            query_params = http_request.query_params or {}
            
            fiscal_id = body['fiscal_id']
            page = body['page']
            page_size = body['page_size']
            search_term = query_params.get('search')  # Opcional para filtro
            
            # Buscar projetos do fiscal com filtro aplicado no repository
            result = self.__get_projects_by_fiscal_with_pagination.get(
                fiscal_id=fiscal_id, 
                page=int(page), 
                page_size=int(page_size),
                search_term=search_term
            )
            
            # Buscar detalhes completos dos projetos (já filtrados)
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
                
                # Buscar última fiscalização e contagem para este projeto
                latest_work_project = self.__work_project_repository.find_latest_by_project(project.project_id)
                work_projects_count_data = self.__work_project_repository.get_work_projects_with_pagination_by_fiscal_and_project(
                    fiscal_id=fiscal_id,
                    project_id=project.project_id,
                    page=1,
                    page_size=1
                )
                
                projects_with_details.append({
                    'id': project.project_id,
                    'status_id': project.status_id,
                    'status_name': project.status.description if project.status else None,
                    'verba_disponivel': verba_value,
                    'andamento_do_projeto': project.andamento_do_projeto,
                    'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else None,
                    'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else None,
                    'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else None,
                    'name': project.name,
                    'bairro_name': project.bairro.name if project.bairro else None,
                    'empresa_name': project.empresas.name if project.empresas else None,
                    'work_project_count': work_projects_count_data.get('total', 0),
                    'last_fiscalizacao_date': latest_work_project.created_at.strftime(r'%d/%m/%Y') if latest_work_project and latest_work_project.created_at else None
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