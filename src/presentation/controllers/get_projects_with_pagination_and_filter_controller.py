#pylint:disable=all
from src.domain.use_cases.i_get_projects_with_pagination_and_filter import IGetProjectsWithPaginationAndFilter
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectsWithPaginationAndFilterController(ControllerInterface):

    def __init__(self, get_projects_with_pagination_and_filter_case: IGetProjectsWithPaginationAndFilter) -> None:
        self.__get_projects_with_pagination_and_filter_case = get_projects_with_pagination_and_filter_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            query_params = http_request.query_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            search_term = query_params.get('search')
            result = self.__get_projects_with_pagination_and_filter_case.get(page_size=int(page_size), page=int(page), search_term=search_term)
            
            # Transformar os dados para o formato esperado
            projects_data = []
            
            # Buscar dados de usuário para todos os projetos de uma vez
            project_ids = [p.project_id for p in result['projects']]
            user_data_dict = {}
            
            if project_ids:
                from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
                from sqlalchemy import text
                
                db_handler = db_connection_handler_factory()
                with db_handler as db:
                    # Query para buscar usuários associados aos projetos
                    placeholders = ','.join([':id' + str(i) for i in range(len(project_ids))])
                    query = text(f"""
                        SELECT up.project_id, u.cpf, u.name, u.email, u.role, u.created_at
                        FROM user_project up
                        JOIN user u ON up.user_cpf = u.cpf
                        WHERE up.project_id IN ({placeholders})
                    """)
                    params = {f'id{i}': project_id for i, project_id in enumerate(project_ids)}
                    user_results = db.session.execute(query, params).fetchall()
                    
                    for row in user_results:
                        project_id, cpf, name, email, role, created_at = row
                        user_data_dict[project_id] = {
                            'cpf': cpf,
                            'name': name,
                            'email': email,
                            'role': role,
                            'created_at': created_at.strftime(r'%d/%m/%Y') if created_at else None
                        }
            
            for project in result['projects']:
                # Buscar dados do usuário no dicionário
                user_data = user_data_dict.get(project.project_id)
                
                project_data = {
                    'id': project.project_id,
                    'name': project.name,
                    'verba_disponivel': float(project.verba_disponivel.value) if project.verba_disponivel else None,
                    'andamento_do_projeto': project.andamento_do_projeto,
                    'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else None,
                    'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else None,
                    'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else None,
                    'status_id': project.status_id,
                    'bairro': {
                        'id': project.bairro.bairro,
                        'name': project.bairro.name,
                        'created_at': project.bairro.created_at.strftime(r'%d/%m/%Y') if project.bairro and project.bairro.created_at else None
                    } if project.bairro else None,
                    'empresa': {
                        'id': project.empresas.empresa_id,
                        'name': project.empresas.name,
                        'created_at': project.empresas.created_at.strftime(r'%d/%m/%Y') if project.empresas and project.empresas.created_at else None
                    } if project.empresas else None,
                    'fiscal': {
                        'id': project.fiscal.fiscal_id,
                        'name': project.fiscal.name,
                        'created_at': project.fiscal.created_at.strftime(r'%d/%m/%Y') if project.fiscal and project.fiscal.created_at else None
                    } if project.fiscal else None,
                    'types': {
                        'id': project.types.types_id,
                        'name': project.types.name,
                        'created_at': project.types.created_at.strftime(r'%d/%m/%Y') if project.types and project.types.created_at else None
                    } if project.types else None,
                    'status': {
                        'id': project.status.status_id,
                        'description': project.status.description,
                        'created_at': project.status.created_at.strftime(r'%d/%m/%Y') if project.status and project.status.created_at else None
                    } if project.status else None,
                    'user': user_data
                }
                projects_data.append(project_data)
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'content': {
                        'page': result['current_page'],
                        'page_size': result['page_size'],
                        'total_items': result['total_items'],
                        'total_pages': result['total_pages'],
                        'projects': projects_data
                    }
                }
            )
        except Exception as e:
            raise e from e
