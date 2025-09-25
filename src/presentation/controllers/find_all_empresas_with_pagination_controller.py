#pylint:disable=all
from src.domain.use_cases.i_find_all_empresas_with_pagination import IFindAllEmpresasWithPagination
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllEmpresasWithPaginationController(ControllerInterface):

    def __init__(self, find_all_empresas_with_pagination_case: IFindAllEmpresasWithPagination) -> None:
        self.__find_all_empresas_with_pagination_case = find_all_empresas_with_pagination_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            page = path_params.get('page')
            page_size = path_params.get('page_size')
            result = self.__find_all_empresas_with_pagination_case.find(page_size=int(page_size), page=int(page))
            
            # Transformar os dados para o formato esperado
            empresas_data = [
                {
                    'id': empresa.empresa_id,
                    'name': empresa.name,
                    'created_at': empresa.created_at.strftime(r'%d/%m/%Y') if empresa.created_at else None
                }
                for empresa in result['empresas']
            ]
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresas Founded',
                    'content': {
                        'page': result['current_page'],
                        'page_size': result['page_size'],
                        'total_items': result['total_items'],
                        'total_pages': result['total_pages'],
                        'empresas': empresas_data
                    }
                }
            )
        except Exception as e:
            raise e from e
