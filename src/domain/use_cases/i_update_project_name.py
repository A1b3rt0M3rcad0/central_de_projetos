from abc import ABC, abstractmethod

class IUpdateProjectName(ABC):

    @abstractmethod
    def update(self, project_id:int, name:str) -> None:
        '''
        Pega project_id e o nome e atuliza o nome do projeto no banco de dados,
        caso não consiga trocar o nome no banco de dados, retorne o error 500, internal server error
        '''