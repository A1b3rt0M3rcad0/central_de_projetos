from abc import ABC, abstractmethod

class IDeleteDocument(ABC):

    @abstractmethod
    def delete(self, project_id:int, document_name:str) -> None:
        """
        Deleta um documento associado a um projeto no banco de dados.

        Parâmetros:
            project_id: ID do projeto ao qual o documento está vinculado.
            document_name: Nome do documento a ser deletado.

        Levanta:
            DocumentNotFoundError (404): Se não for encontrado um documento com o nome informado no projeto.
        """