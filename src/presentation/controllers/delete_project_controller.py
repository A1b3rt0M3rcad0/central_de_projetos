from src.domain.use_cases.i_delete_project import IDeleteProject
from src.domain.use_cases.i_delete_all_history_project_from_project import IDeleteAllHistoryProjectFromProject
from src.domain.use_cases.i_delete_association_user_from_project import IDeleteAssociationUserFromProject
from src.domain.use_cases.i_delete_bairro_from_project import IDeleteBairroFromProject
from src.domain.use_cases.i_delete_empresa_from_project import IDeleteEmpresaFromProject
from src.domain.use_cases.i_delete_fiscal_from_project import IDeleteFiscalFromProject
from src.domain.use_cases.i_delete_type_from_project import IDeleteTypeFromProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectController(ControllerInterface):

    def __init__(self, 
                 delete_project_case:IDeleteProject,
                 delete_all_history_project_from_project_case:IDeleteAllHistoryProjectFromProject,
                 delete_association_user_from_project_case:IDeleteAssociationUserFromProject,
                 delete_bairro_from_project_case:IDeleteBairroFromProject,
                 delete_empresa_from_project_case:IDeleteEmpresaFromProject,
                 delete_fiscal_from_project_case:IDeleteFiscalFromProject,
                 delete_type_from_project_case:IDeleteTypeFromProject
                 ) -> None:
        self.__delete_project_case = delete_project_case
        self.__delete_all_history_project_from_project_case = delete_all_history_project_from_project_case
        self.__delete_association_user_from_project_case = delete_association_user_from_project_case
        self.__delete_bairro_from_project_case = delete_bairro_from_project_case
        self.__delete_empresa_from_project_case = delete_empresa_from_project_case
        self.__delete_fiscal_from_project_case = delete_fiscal_from_project_case
        self.__delete_type_from_project_case = delete_type_from_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            #history_project
            self.__delete_all_history_project_from_project_case.delete(
                project_id=project_id
            )
            
            #project user
            self.__delete_association_user_from_project_case.delete(
                project_id=project_id
            )

            #project bairro
            self.__delete_bairro_from_project_case.delete(
                project_id=project_id
            )

            #project empresa
            self.__delete_empresa_from_project_case.delete(
                project_id=project_id
            )

            # project fiscal
            self.__delete_fiscal_from_project_case.delete(
                project_id=project_id
            )

            # project type
            self.__delete_type_from_project_case.delete(
                project_id=project_id
            )

            #project
            self.__delete_project_case.delete(
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Deleted'
                }
            )
        except Exception as e:
            raise e from e