from typing import List
from abc import ABC, abstractmethod

class IGetDocumentNames(ABC):

    @abstractmethod
    def names(self, project_id:int) -> List[str]:
        '''
        Coleta o numero do projeto para retornar uma lista dos nomes dos arquivos do projeto,
        caso não encontre nenhum nome retorn um erro chamado 401, DocumentsNotFoundedError
        '''