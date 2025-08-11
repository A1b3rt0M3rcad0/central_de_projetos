from abc import ABC, abstractmethod
from typing import Optional

class IGetLatestWorkProjectImage(ABC):

    @abstractmethod
    def get_latest_image(self, work_project_id: int) -> Optional[bytes]:
        """
        Obtém a última imagem enviada para o work project.
        
        Parâmetros:
            work_project_id: ID do work project.
            
        Retorna:
            Optional[bytes]: Imagem em bytes ou None se não houver imagens.
            
        Levanta:
            WorkProjectNotFoundError: Se o work project não for encontrado.
        """ 