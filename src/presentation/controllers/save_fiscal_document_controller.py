from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_save_fiscal_document import ISaveFiscalDocument
from src.domain.value_objects.document import Document
from typing import List

class SaveFiscalDocumentController(ControllerInterface):

    def __init__(self, save_fiscal_document_case:ISaveFiscalDocument) -> None:
        self.__save_fiscal_document_case = save_fiscal_document_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.query_params.get('project_id')
            fiscal_id = http_request.query_params.get('fiscal_id')
            documents = http_request.files
            
            # Convert files to Document objects
            document_list: List[Document] = []
            for file in documents:
                document = Document(
                    document_name=file.filename,
                    value=file.file.read(),
                    content_type=file.content_type
                )
                document_list.append(document)

            self.__save_fiscal_document_case.save(
                project_id=int(project_id),
                fiscal_id=int(fiscal_id),
                documents=document_list
            )

            return HttpResponse(
                status_code=201,
                body={"message": "Fiscal documents saved successfully"}
            )

        except Exception as e:
            raise e from e