from abc import ABC, abstractmethod

class IDeleteWorkProjectFromProject(ABC):
    
    @abstractmethod
    def delete(self, project_id: int) -> None:
        """
        Remove todos os work_projects de um projeto
        
        Args:
            project_id: ID do projeto
        """
        pass

