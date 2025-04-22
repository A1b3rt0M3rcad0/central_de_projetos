from src.domain.value_objects.document import Document
from abc import ABC, abstractmethod

class IGetDocument(ABC):

    @abstractmethod
    def document(self, project_id:int, document_name:str, _document_class:Document=Document) -> Document:
        """
        Retorna o documento associado ao projeto e ao nome do documento fornecido.

        Parâmetros:
            project_id: ID do projeto para o qual o documento será recuperado.
            document_name: Nome do documento a ser recuperado.
            _document_class: Classe do documento a ser retornado (padrão: Document).

        Retorno:
            Instância de Document representando o documento encontrado.

        Levanta:
            DocumentNotFoundError (404): Se o documento com o nome especificado não for encontrado.
            InternalServerError (500): Para qualquer outro erro durante a operação.
        """