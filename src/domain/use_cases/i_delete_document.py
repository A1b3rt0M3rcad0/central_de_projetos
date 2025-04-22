from abc import ABC, abstractmethod

class IDeleteDocument(ABC):

    @abstractmethod
    def delete(self, project_id:int, document_name:str) -> None:
        '''
        Pega o project_id e o nome do documento, para relizar a deleção do documento no banco de dados do projeto,
        caso não tenha encontrado um documento com o nome buscado, retorne o erro 404, DocumentNotFoundedError
        '''