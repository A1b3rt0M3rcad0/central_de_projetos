from abc import ABC, abstractmethod

class IUpdateType(ABC):

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:
        '''
        Faz o update do nome do typo no db

        Parãmetros;
            name: nome do typo para busca
            new_name: nome do typo para atualização
        Levanta:
            None
        '''