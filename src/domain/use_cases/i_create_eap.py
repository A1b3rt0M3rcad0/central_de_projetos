from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.eap import EAPEntity


class ICreateEAP(ABC):
    """Interface para o caso de uso de criação de EAP"""
    
    @abstractmethod
    def create(self, name: str, description: str, project_id: int, created_by: str, template_source_id: Optional[int] = None) -> EAPEntity:
        """
        Cria uma nova EAP
        
        Args:
            name: Nome da EAP
            description: Descrição da EAP
            project_id: ID do projeto ao qual a EAP será vinculada
            created_by: ID do usuário que está criando a EAP
            template_source_id: ID da EAP template que será usada como base (opcional)
        
        Returns:
            EAPEntity: A EAP criada
            
        Raises:
            ValueError: Se os dados fornecidos forem inválidos
            ProjectNotFoundError: Se o projeto não existir
            EAPTemplateNotFoundError: Se a EAP template não existir
            ProjectAlreadyHasEAPError: Se o projeto já possui uma EAP
        """
        pass
