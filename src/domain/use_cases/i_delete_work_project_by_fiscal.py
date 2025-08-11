from abc import ABC, abstractmethod

class IDeleteWorkProjectByFiscal(ABC):

    @abstractmethod
    def delete(self, work_project_id:int, fiscal_id:int) -> None:
        '''
        Deleta um work project e seus documentos associados.
        Apenas o fiscal associado ao work project pode deletá-lo.

        Parâmetros:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal que está tentando deletar
            
        Levanta:
            WorkProjectNotExists: Se o work project não existir
            FiscalNotAuthorizedError: Se o fiscal não estiver associado ao work project
            ErrorOnDeleteWorkProject: Caso ocorra qualquer erro relacionado à deleção
        ''' 