#pylint:disable=W0718
from src.domain.use_cases.i_delete_project import IDeleteProject
from src.domain.use_cases.i_delete_all_history_project_from_project import IDeleteAllHistoryProjectFromProject
from src.domain.use_cases.i_delete_association_user_from_project import IDeleteAssociationUserFromProject
from src.domain.use_cases.i_delete_bairro_from_project import IDeleteBairroFromProject
from src.domain.use_cases.i_delete_empresa_from_project import IDeleteEmpresaFromProject
from src.domain.use_cases.i_delete_fiscal_from_project import IDeleteFiscalFromProject
from src.domain.use_cases.i_delete_type_from_project import IDeleteTypeFromProject
from src.domain.use_cases.i_delete_folder_from_project import IDeleteFolderFromProject
from src.domain.use_cases.i_delete_work_project_from_project import IDeleteWorkProjectFromProject
from src.domain.use_cases.i_delete_eap_from_project import IDeleteEAPFromProject
from src.domain.use_cases.i_delete_all_documents_from_project import IDeleteAllDocumentsFromProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectController(ControllerInterface):

    def __init__(
        self, 
        delete_project_case: IDeleteProject,
        delete_all_history_project_from_project_case: IDeleteAllHistoryProjectFromProject,
        delete_association_user_from_project_case: IDeleteAssociationUserFromProject,
        delete_bairro_from_project_case: IDeleteBairroFromProject,
        delete_empresa_from_project_case: IDeleteEmpresaFromProject,
        delete_fiscal_from_project_case: IDeleteFiscalFromProject,
        delete_type_from_project_case: IDeleteTypeFromProject,
        delete_folder_from_project_case: IDeleteFolderFromProject,
        delete_work_project_from_project_case: IDeleteWorkProjectFromProject,
        delete_eap_from_project_case: IDeleteEAPFromProject,
        delete_all_documents_from_project_case: IDeleteAllDocumentsFromProject,
    ) -> None:
        self.__delete_project_case = delete_project_case
        self.__delete_all_history_project_from_project_case = delete_all_history_project_from_project_case
        self.__delete_association_user_from_project_case = delete_association_user_from_project_case
        self.__delete_bairro_from_project_case = delete_bairro_from_project_case
        self.__delete_empresa_from_project_case = delete_empresa_from_project_case
        self.__delete_fiscal_from_project_case = delete_fiscal_from_project_case
        self.__delete_type_from_project_case = delete_type_from_project_case
        self.__delete_folder_from_project_case = delete_folder_from_project_case
        self.__delete_work_project_from_project_case = delete_work_project_from_project_case
        self.__delete_eap_from_project_case = delete_eap_from_project_case
        self.__delete_all_documents_from_project_case = delete_all_documents_from_project_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.body.get('project_id')
            if not project_id:
                return HttpResponse(status_code=400, body={"error": "project_id is required"})

            # IMPORTANTE: Ordem de deleção - deletar dependências ANTES do projeto
            delete_operations = [
                ("delete_all_history_project_from_project_case", self.__delete_all_history_project_from_project_case),
                ("delete_association_user_from_project_case", self.__delete_association_user_from_project_case),
                ("delete_bairro_from_project_case", self.__delete_bairro_from_project_case),
                ("delete_empresa_from_project_case", self.__delete_empresa_from_project_case),
                ("delete_fiscal_from_project_case", self.__delete_fiscal_from_project_case),
                ("delete_type_from_project_case", self.__delete_type_from_project_case),
                ("delete_folder_from_project_case", self.__delete_folder_from_project_case),
                ("delete_work_project_from_project_case", self.__delete_work_project_from_project_case),
                ("delete_eap_from_project_case", self.__delete_eap_from_project_case),
                ("delete_all_documents_from_project_case", self.__delete_all_documents_from_project_case),
                # Deletar o projeto por último, após todas as dependências
                ("delete_project_case", self.__delete_project_case),
            ]

            for name, use_case in delete_operations:
                try:
                    use_case.delete(project_id=project_id)
                except Exception as e:
                    print(f"Warning: Failed to execute {name}. Reason: {str(e)}")
                    # aplicar logger se necessário

            return HttpResponse(
                status_code=200,
                body={"message": "Project deleted successfully"}
            )

        except Exception as e:
            raise e from e