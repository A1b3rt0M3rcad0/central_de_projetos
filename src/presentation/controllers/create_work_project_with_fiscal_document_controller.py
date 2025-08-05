from src.domain.use_cases.i_insert_work_project import IInsertWorkProject
from src.domain.use_cases.i_save_fiscal_document import ISaveFiscalDocument
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.generic_document import GenericDocument


class CreateWorkProjectWithFiscalDocumentController(ControllerInterface):

    def __init__(self, 
                 insert_work_project_case: IInsertWorkProject,
                 save_fiscal_document_case: ISaveFiscalDocument) -> None:
        self.__insert_work_project_case = insert_work_project_case
        self.__save_fiscal_document_case = save_fiscal_document_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            
            # Dados do work project
            project_id = body['project_id']
            fiscal_id = body['fiscal_id']
            title = body['title']
            description = body['description']
            
            # Processar documentos fiscais do multipart_adapter
            documents = []
            photo_name = None
            additional_documents = None
            
            # O multipart_adapter envia os documentos em 'additional_documents'
            if 'additional_documents' in body and body['additional_documents']:
                document_names = []
                
                for doc_data in body['additional_documents']:
                    # O multipart_adapter envia: name, content, content_type
                    document = GenericDocument(
                        document=doc_data['content'],  # bytes do arquivo
                        content_type=doc_data['content_type'],  # str
                        name=doc_data['name'],  # str (nome interno)
                        document_name=doc_data['name']  # str (nome original do arquivo)
                    )
                    documents.append(document)
                    document_names.append(doc_data['name'])
                    
                    # Se for uma imagem, usar como photo_name
                    if doc_data['content_type'].startswith('image/'):
                        photo_name = doc_data['name']
                
                # Criar additional_documents com a lista de nomes dos documentos
                additional_documents = ", ".join(document_names)
            
            # Se não houver foto específica, usar o primeiro documento como foto
            if not photo_name and documents:
                photo_name = documents[0].document_name
            
            # Criar o work project
            work_project_id = self.__insert_work_project_case.insert(
                project_id=project_id,
                fiscal_id=fiscal_id,
                title=title,
                description=description,
                photo_name=photo_name,
                additional_documents=additional_documents
            )
            
            # Salvar documentos fiscais se houver
            if documents:
                self.__save_fiscal_document_case.save(
                    work_project_id=work_project_id,
                    fiscal_id=fiscal_id,
                    documents=documents
                )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work project created with fiscal documents successfully',
                    'title': title,
                    'photo_name': photo_name,
                    'documents_count': len(documents)
                }
            )

        except Exception as e:
            raise e from e 