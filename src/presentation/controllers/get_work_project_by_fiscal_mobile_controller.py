from src.domain.use_cases.i_get_work_project_by_fiscal import IGetWorkProjectByFiscal
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class GetWorkProjectByFiscalMobileController(ControllerInterface):

    def __init__(self, get_work_project_by_fiscal_case: IGetWorkProjectByFiscal) -> None:
        self.__get_work_project_by_fiscal_case = get_work_project_by_fiscal_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            work_project_id = body['work_project_id']
            fiscal_id = body['fiscal_id']
            
            work_project = self.__get_work_project_by_fiscal_case.get(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id
            )
            
            # Construir lista de documentos combinando photo_name e additional_documents
            documents = []
            if work_project.photo_name:
                documents.append({'name': work_project.photo_name, 'type': 'photo'})
            if work_project.additional_documents:
                for doc_name in work_project.additional_documents:
                    documents.append({'name': doc_name, 'type': 'additional'})
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work Project found successfully',
                    'content': {
                        'id': work_project.id,
                        'project_id': work_project.project_id,
                        'fiscal_id': work_project.fiscal_id,
                        'title': work_project.title,
                        'description': work_project.description,
                        'photo_name': work_project.photo_name,
                        'additional_documents': work_project.additional_documents,
                        'documents': documents,
                        'created_at': work_project.created_at.strftime(r'%d/%m/%Y %H:%M:%S'),
                        'updated_at': work_project.updated_at.strftime(r'%d/%m/%Y %H:%M:%S'),
                        'fiscal': {
                            'id': work_project.fiscal.fiscal_id,
                            'name': work_project.fiscal.name,
                            'created_at': work_project.fiscal.created_at.strftime(r'%d/%m/%Y %H:%M:%S')
                        } if work_project.fiscal else None,
                        'project': {
                            'id': work_project.project.project_id,
                            'status_id': work_project.project.status_id,
                            'name': work_project.project.name,
                            'andamento_do_projeto': work_project.project.andamento_do_projeto,
                            'verba_disponivel': str(work_project.project.verba_disponivel),
                            'start_date': work_project.project.start_date.strftime(r'%d/%m/%Y') if work_project.project.start_date else None,
                            'expected_completion_date': work_project.project.expected_completion_date.strftime(r'%d/%m/%Y') if work_project.project.expected_completion_date else None,
                            'end_date': work_project.project.end_date.strftime(r'%d/%m/%Y') if work_project.project.end_date else None
                        } if work_project.project else None
                    }
                }
            )
        except Exception as e:
            raise e from e 