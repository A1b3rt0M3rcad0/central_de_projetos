from abc import ABC, abstractmethod

class IUpdateBairroName(ABC):

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:
        '''
        Faz a atualização do nome do bairro

        Parãmetros:
            name: nome antigo do bairro
            new_name: novo nome atualizado do bairro
        Levanta:
            Exception
        '''