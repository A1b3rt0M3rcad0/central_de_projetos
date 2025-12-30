#pylint:disable=all
from src.domain.use_cases.i_find_all_folders_with_pagination import IFindAllFoldersWithPagination
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.data.interface.i_folder_repository import IFolderRepository

class FindAllFoldersWithPaginationController(ControllerInterface):

    def __init__(self, find_all_folders_with_pagination_case: IFindAllFoldersWithPagination, folder_repository: IFolderRepository) -> None:
        self.__find_all_folders_with_pagination_case = find_all_folders_with_pagination_case
        self.__folder_repository = folder_repository

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            page = int(path_params.get('page'))
            page_size = int(path_params.get('page_size'))
            result = self.__find_all_folders_with_pagination_case.find(page=page, page_size=page_size)
            
            total_items = self.__folder_repository.count_all()
            total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
            
            folders_data = [
                {
                    'id': folder.folder_id,
                    'name': folder.name,
                    'created_at': folder.created_at.strftime(r'%d/%m/%Y') if folder.created_at else None,
                    'updated_at': folder.updated_at.strftime(r'%d/%m/%Y') if folder.updated_at else None
                }
                for folder in result
            ]
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folders Founded',
                    'content': {
                        'page': page,
                        'page_size': page_size,
                        'total_items': total_items,
                        'total_pages': total_pages,
                        'folders': folders_data
                    }
                }
            )
        except Exception as e:
            raise e from e

