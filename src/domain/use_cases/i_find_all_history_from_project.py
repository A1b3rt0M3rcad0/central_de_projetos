from abc import ABC, abstractmethod
from src.domain.entities.history_project import HistoryProjectEntity
from typing import List

class IFindAllHistoryFromProject(ABC):

    @abstractmethod
    def find(self, project_id:int) -> List[HistoryProjectEntity]:
        '''
        Coleta todo o historico demodificações do projeto em uma lista de entidades do domain,
        caso não encontreo projeto retorna 404, ProjectNotFound
        qualquer outro erro retorna 500 InternalServerError
        '''