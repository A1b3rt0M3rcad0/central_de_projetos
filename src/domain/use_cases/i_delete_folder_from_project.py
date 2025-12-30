from abc import ABC, abstractmethod

class IDeleteFolderFromProject(ABC):
    
    @abstractmethod
    def delete(self, project_id: int) -> None:
        """
        Remove todas as associações de pastas de um projeto
        
        Args:
            project_id: ID do projeto
        """
        pass

