from abc import ABC, abstractmethod

class IUpdateBairroFromProject(ABC):

    @abstractmethod
    def update(self, project_id:int, bairro_id:int, new_bairro_id:int) -> None:
        '''
        Troca o bairro do projeto por outro bairro existente

        Parâmetros:
            project_id: ID do projeto
            bairro_id: ID do bairro:
            new_bairro_id: ID do novo bairro
        Levanta:
            ErrorOnUpdateBairroFromProject; caso tenha ocorrido qualquer erro na hora de dar update no bairro
        '''