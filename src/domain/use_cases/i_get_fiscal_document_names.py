from typing import List
from abc import ABC, abstractmethod

class IGetFiscalDocumentNames(ABC):

    @abstractmethod
    def get_names(self, work_project_id:int, fiscal_id:int) -> List[str]:
        """
        Lista todos os nomes dos documentos enviados por um fiscal para um work project.

        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal

        Returns:
            List[str]: Lista com os nomes dos documentos

        Raises:
            FiscalDocumentNamesNotFoundError (404): Se não forem encontrados documentos
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            WorkProjectNotFoundError (404): Se o work project não for encontrado
            InternalServerError (500): Para qualquer outro erro durante a operação
        """