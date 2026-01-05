from abc import ABC, abstractmethod

class IDeleteEAPFromProject(ABC):
    
    @abstractmethod
    def delete(self, project_id: int) -> None:
        """
        Remove todas as EAPs de um projeto
        
        Args:
            project_id: ID do projeto
        """
        pass

