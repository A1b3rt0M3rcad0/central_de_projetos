from abc import ABC, abstractmethod

class ICountFolders(ABC):

    @abstractmethod
    def count(self, search_term: str = None) -> int:
        '''
        Conta o total de pastas no sistema

        Parâmetros:
            search_term: termo de busca opcional para filtrar por nome
        Retorna:
            Número total de pastas
        '''

