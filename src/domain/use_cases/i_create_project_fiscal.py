from abc import ABC, abstractmethod

class ICreateProjectFiscal(ABC):

    @abstractmethod
    def create(self, project_id:int, fiscal_id:int) -> None:
        '''
        Associa um projeto a um fiscal

        Parâmetros:
            project_id: ID do projeto que sera associado ao fiscal
            fiscal_id: ID do fiscal que sera associado a o projeto
        
        Levanta:
            ProjectFiscalAlreadyExists: Caso a associação do projeto não possa ser criada, pois ja existe uma
        '''