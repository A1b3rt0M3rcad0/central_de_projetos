from abc import ABC, abstractmethod

class IDeleteProjectBairro(ABC):

    @abstractmethod
    def delete(self, project_id:int, bairro_id:int) -> None:
        '''
        Deleta uma associação bairro projeto

        Parametros:
            project_id: ID do projeto
            bairr_id; ID do bairro
        Levanta:
            ErrorOnDeleteProjectBairro: Caso ocorra qualquer erro na deleção do projeto
        '''