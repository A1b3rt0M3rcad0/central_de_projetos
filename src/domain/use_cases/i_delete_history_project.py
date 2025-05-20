from abc import ABC, abstractmethod

class IDeleteHistoryProject(ABC):

    @abstractmethod
    def delete(self, history_project_id:int) -> None:
        '''
        Deleta o hisotry project de acordoc seu id
        '''