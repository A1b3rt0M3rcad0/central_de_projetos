from abc import ABC, abstractmethod
from typing import Optional

class ICreateHistoryProject(ABC):

    @abstractmethod
    def create(self, project_id:int, data_name:str, description:Optional[str]=None) -> None:
        '''
        Cria um historico de modificações do projeto no banco de dados, para cada alteração de dados, ou adição de documentos
        é criado um historico do projeto.
        caso não consiga criar um historico do projeto pois o project_id não existe,
        lança um erro 404, ProjectNotFoundError
        qualquer outro erro, lança 500 InternalServerError
        '''