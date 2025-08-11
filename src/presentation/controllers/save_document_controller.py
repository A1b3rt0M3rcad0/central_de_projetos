from src.domain.use_cases.i_save_document import ISaveDocument
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.generic_document import GenericDocument


class SaveDocumentController(ControllerInterface):

    def __init__(self, 
                 save_document_use_case: ISaveDocument,
                 create_history_project_case: ICreateHistoryProject) -> None:
        self.__save_document_use_case = save_document_use_case
        self.__create_history_project_case = create_history_project_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']

            document = GenericDocument(
                document=body["document"],                  # bytes
                content_type=body["content_type"],          # str
                name=body["name"],                          # str (nome interno)
                document_name=body["document_name"]         # str (nome original ou exibido)
            )

            self.__save_document_use_case.save(
                document=[document],
                project_id=project_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Documento',
                description=f'Documento "{body["document_name"]}" adicionado ao projeto'
            )

            return HttpResponse(
                status_code=200,
                body={"message": "Document uploaded successfully", "name": body["document_name"]}
            )

        except Exception as e:
            raise e from e