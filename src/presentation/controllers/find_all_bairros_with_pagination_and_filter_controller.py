#pylint:disable=all
from src.domain.use_cases.i_find_all_bairros_with_pagination_and_filter import IFindAllBairrosWithPaginationAndFilter
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllBairrosWithPaginationAndFilterController(ControllerInterface):

    def __init__(self, find_all_bairros_with_pagination_and_filter_case: IFindAllBairrosWithPaginationAndFilter) -> None:
        self.__find_all_bairros_with_pagination_and_filter_case = find_all_bairros_with_pagination_and_filter_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            query_params = http_request.query_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            search_term = query_params.get('search')
            result = self.__find_all_bairros_with_pagination_and_filter_case.find(page_size=int(page_size), page=int(page), search_term=search_term)
            
            # Transformar os dados para o formato esperado
            bairros_data = [
                {
                    'id': bairro.bairro,
                    'name': bairro.name,
                    'created_at': bairro.created_at.strftime(r'%d/%m/%Y') if bairro.created_at else None
                }
                for bairro in result['bairros']
            ]
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairros Founded',
                    'content': {
                        'page': result['current_page'],
                        'page_size': result['page_size'],
                        'total_items': result['total_items'],
                        'total_pages': result['total_pages'],
                        'bairros': bairros_data
                    }
                }
            )
        except Exception as e:
            raise e from e
