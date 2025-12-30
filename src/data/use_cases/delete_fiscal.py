from src.domain.use_cases.i_delete_fiscal import IDeleteFiscal
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.data.interface.i_project_fiscal_repository import IProjectFiscalRepository
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class DeleteFiscal(IDeleteFiscal):

    def __init__(
        self, 
        fiscal_repository:IFiscalRepository,
        project_fiscal_repository:IProjectFiscalRepository,
        work_project_repository:IWorkProjectRepository,
        project_document_fiscal_repository:IProjectDocumentFiscalRepository
    ) -> None:
        self.__fiscal_repository = fiscal_repository
        self.__project_fiscal_repository = project_fiscal_repository
        self.__work_project_repository = work_project_repository
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete(self, name:str) -> None:
        try:
            # 1. Buscar o fiscal para obter o ID
            fiscal = self.__fiscal_repository.find_by_name(name=name)
            fiscal_id = fiscal.fiscal_id
            
            # 2. Buscar todos os work projects do fiscal para deletar documentos
            work_projects = self.__work_project_repository.find_by_fiscal(fiscal_id=fiscal_id)
            work_project_ids = [wp.id for wp in work_projects]
            
            # 3. Deletar todos os documentos fiscais dos work projects (RavenDB)
            if work_project_ids:
                self.__project_document_fiscal_repository.delete_all_fiscal_documents_from_fiscal(
                    fiscal_id=fiscal_id,
                    work_project_ids=work_project_ids
                )
            
            # 4. Deletar todos os work projects do fiscal
            self.__work_project_repository.delete_all_from_fiscal(fiscal_id=fiscal_id)
            
            # 5. Deletar todas as associações projeto-fiscal
            self.__project_fiscal_repository.delete_all_from_fiscal(fiscal_id=fiscal_id)
            
            # 6. Finalmente, deletar o fiscal
            self.__fiscal_repository.delete(name=name)
        except Exception as e:
            raise e from e