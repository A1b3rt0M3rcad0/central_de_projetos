from src.domain.use_cases.i_save_fiscal_document import ISaveFiscalDocument
from src.domain.use_cases.i_update_work_project_documents import IUpdateWorkProjectDocuments
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.generic_document import GenericDocument
import json

class AddDocumentsToWorkProjectController(ControllerInterface):
    
    def __init__(self, 
                 save_fiscal_document_case: ISaveFiscalDocument,
                 update_work_project_documents_case: IUpdateWorkProjectDocuments,
                 get_work_project_case: IGetWorkProject) -> None:
        self.__save_fiscal_document_case = save_fiscal_document_case
        self.__update_work_project_documents_case = update_work_project_documents_case
        self.__get_work_project_case = get_work_project_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            work_project_id = body['work_project_id']
            documents_data = body.get('documents', body.get('additional_documents', []))  # Suporta ambos os formatos
            
            # Validação: Verificar se o work_project existe
            try:
                self.__get_work_project_case.get(work_project_id=work_project_id)
            except Exception as e:
                raise e from e
            
            # Converter dados do frontend para objetos GenericDocument
            documents = []
            for doc_data in documents_data:
                # Assumindo que o frontend envia base64 ou dados binários
                document = GenericDocument(
                    document=doc_data['content'],
                    document_name=doc_data['name'],
                    content_type=doc_data['content_type']
                )
                documents.append(document)
            
            # 1. Salvar documentos no RavenDB (SaveFiscalDocument)
            self.__save_fiscal_document_case.save(
                work_project_id=work_project_id,
                documents=documents
            )
            
            # 2. Atualizar additional_documents no work_project (UpdateWorkProjectDocuments)
            # Criar lista de nomes dos documentos para adicionar ao JSON
            document_names = [doc.document_name for doc in documents]
            
            self.__update_work_project_documents_case.update(
                work_project_id=work_project_id,
                additional_documents=json.dumps(document_names)
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': f'Documents added successfully to work project {work_project_id}',
                    'documents_added': document_names
                }
            )
            
        except Exception as e:
            raise e from e 