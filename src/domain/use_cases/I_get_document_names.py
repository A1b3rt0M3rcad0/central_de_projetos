from typing import List
from abc import ABC, abstractmethod

class IGetDocumentNames(ABC):

    @abstractmethod
    def names(self, project_id:int) -> List[str]:
        """
        Retorna uma lista com os nomes dos documentos associados ao projeto.

        Parâmetros:
            project_id: ID do projeto para o qual os documentos serão recuperados.

        Retorno:
            Lista de strings contendo os nomes dos documentos associados ao projeto.

        Levanta:
            DocumentsNotFoundError (404): Se não forem encontrados documentos associados ao projeto.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """