#pylint:disable=all
from src.domain.use_cases.i_find_all_users_with_pagination import IFindAllUsersWithPagination
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllUsersWithPaginationController(ControllerInterface):

    def __init__(self, find_all_users_with_pagination_case: IFindAllUsersWithPagination) -> None:
        self.__find_all_users_with_pagination_case = find_all_users_with_pagination_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            result = self.__find_all_users_with_pagination_case.find(page_size=int(page_size), page=int(page))
            
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
