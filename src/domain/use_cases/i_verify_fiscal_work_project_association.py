from abc import ABC, abstractmethod

class IVerifyFiscalWorkProjectAssociation(ABC):

    @abstractmethod
    def verify(self, fiscal_id: int, work_project_id: int) -> bool:
        '''
        Verifica se um fiscal está associado a um work project

        Parâmetros:
            fiscal_id: ID do fiscal
            work_project_id: ID do work project
        
        Retorna:
            bool: True se o fiscal está associado ao work project, False caso contrário
        ''' 