from typing import List
from abc import ABC, abstractmethod

class IGetFiscalDocumentNames(ABC):

    @abstractmethod
    def get_names(self, project_id:int, fiscal_id:int) -> List[str]:
        """
        Lista todos os nomes dos documentos enviados por um fiscal para um projeto.

        Args:
            project_id: ID do projeto
            fiscal_id: ID do fiscal

        Returns:
            List[str]: Lista com os nomes dos documentos

        Raises:
            FiscalDocumentNamesNotFoundError (404): Se não forem encontrados documentos
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            ProjectNotFoundError (404): Se o projeto não for encontrado
            InternalServerError (500): Para qualquer outro erro durante a operação
        """