from src.domain.use_cases.i_verify_fiscal_work_project_association import IVerifyFiscalWorkProjectAssociation
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class VerifyFiscalWorkProjectAssociation(IVerifyFiscalWorkProjectAssociation):

    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def verify(self, fiscal_id: int, work_project_id: int) -> bool:
        try:
            # Busca o work project
            work_project = self.__work_project_repository.find(work_project_id)
            
            # Verifica se o fiscal_id do work project é igual ao fiscal_id fornecido
            return work_project.fiscal_id == fiscal_id
        except Exception:
            # Se não encontrar o work project ou qualquer outro erro, retorna False
            return False 