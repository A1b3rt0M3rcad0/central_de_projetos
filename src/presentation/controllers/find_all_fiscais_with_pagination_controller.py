#pylint:disable=all
from src.domain.use_cases.i_find_all_fiscais_with_pagination import IFindAllFiscaisWithPagination
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllFiscaisWithPaginationController(ControllerInterface):

    def __init__(self, find_all_fiscais_with_pagination_case: IFindAllFiscaisWithPagination) -> None:
        self.__find_all_fiscais_with_pagination_case = find_all_fiscais_with_pagination_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            result = self.__find_all_fiscais_with_pagination_case.find(page_size=int(page_size), page=int(page))
            
            # Transformar os dados para o formato esperado
            fiscais_data = [
                {
                    'id': fiscal.fiscal_id,
                    'name': fiscal.name,
                    'email': fiscal.email.email if fiscal.email else None,
                    'phone': fiscal.phone,
                    'created_at': fiscal.created_at.strftime(r'%d/%m/%Y') if fiscal.created_at else None
                }
                for fiscal in result['fiscais']
            ]
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscais Founded',
                    'content': {
                        'page': result['current_page'],
                        'page_size': result['page_size'],
                        'total_items': result['total_items'],
                        'total_pages': result['total_pages'],
                        'fiscais': fiscais_data
                    }
                }
            )
        except Exception as e:
            raise e from e
