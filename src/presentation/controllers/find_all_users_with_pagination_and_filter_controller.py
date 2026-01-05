#pylint:disable=all
from src.domain.use_cases.i_find_all_users_with_pagination_and_filter import IFindAllUsersWithPaginationAndFilter
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllUsersWithPaginationAndFilterController(ControllerInterface):

    def __init__(self, find_all_users_with_pagination_and_filter_case: IFindAllUsersWithPaginationAndFilter) -> None:
        self.__find_all_users_with_pagination_and_filter_case = find_all_users_with_pagination_and_filter_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            query_params = http_request.query_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            search_term = query_params.get('search')
            result = self.__find_all_users_with_pagination_and_filter_case.find(page_size=int(page_size), page=int(page), search_term=search_term)
            
            # Transformar os dados para o formato esperado
            users_data = [
                {
                    'cpf': user.cpf.value,
                    'name': user.name,
                    'email': user.email.email,
                    'role': user.role.value,
                    'created_at': user.created_at.strftime(r'%d/%m/%Y') if user.created_at else None
                }
                for user in result['users']
            ]
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Users Founded',
                    'content': {
                        'page': result['current_page'],
                        'page_size': result['page_size'],
                        'total_items': result['total_items'],
                        'total_pages': result['total_pages'],
                        'users': users_data
                    }
                }
            )
        except Exception as e:
            raise e from e
